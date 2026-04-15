/**
 * Shared WebSocket proxy logic used by both dev (server.ts) and prod (server.prod.mjs) servers.
 *
 * **Producción:** `lib/ws-proxy.mjs` se genera desde este archivo (`pnpm build:ws-proxy`, encadenado en `pnpm build`). No editar el `.mjs` a mano.
 *
 * Proxies a client WebSocket connection to an upstream gateway,
 * buffering messages during upstream connection and forwarding close codes.
 *
 * When device identity is available the proxy transparently injects a signed
 * `device` field into the browser's `connect` handshake frame so the gateway
 * accepts the connection without the browser needing access to the private key.
 */

import crypto from "crypto";
import fs from "fs";
import path from "path";
import { type IncomingMessage } from "http";
import type { Duplex } from "stream";
import { RawData, WebSocket, WebSocketServer } from "ws";
import { createLogger } from "./logger";

const proxyLog = createLogger("WS Proxy");

const MAX_BUFFERED_MESSAGES = 100;
const UPSTREAM_CONNECT_TIMEOUT_MS = 15_000;

// ── Device identity helpers ──────────────────────────────

interface DeviceIdentity {
  deviceId: string;
  publicKeyPem: string;
  privateKeyPem: string;
}

function base64UrlEncode(buf: Buffer): string {
  return buf.toString("base64").replaceAll("+", "-").replaceAll("/", "_").replace(/=+$/g, "");
}

function publicKeyRawBase64Url(pem: string): string {
  const spki = crypto.createPublicKey(pem).export({ type: "spki", format: "der" });
  const ED25519_SPKI_PREFIX_LEN = 12;
  return base64UrlEncode(spki.subarray(ED25519_SPKI_PREFIX_LEN));
}

function signDevicePayload(privateKeyPem: string, payload: string): string {
  const key = crypto.createPrivateKey(privateKeyPem);
  return base64UrlEncode(crypto.sign(null, Buffer.from(payload, "utf8"), key));
}

interface DeviceAuth {
  identity: DeviceIdentity;
  operatorToken: string | null;
}

function loadDeviceAuth(): DeviceAuth | null {
  try {
    const stateDir = path.join(process.env.HOME ?? "", ".openclaw");
    const idRaw = fs.readFileSync(path.join(stateDir, "identity", "device.json"), "utf-8");
    const identity = JSON.parse(idRaw) as DeviceIdentity;
    if (!identity.deviceId || !identity.publicKeyPem || !identity.privateKeyPem) return null;

    let operatorToken: string | null = null;
    try {
      const authRaw = fs.readFileSync(path.join(stateDir, "identity", "device-auth.json"), "utf-8");
      const authData = JSON.parse(authRaw);
      operatorToken = authData.tokens?.operator?.token ?? null;
    } catch {}

    return { identity, operatorToken };
  } catch {}
  return null;
}

let _cachedAuth: DeviceAuth | null | undefined;
function getDeviceAuth(): DeviceAuth | null {
  if (_cachedAuth === undefined) {
    _cachedAuth = loadDeviceAuth();
    if (_cachedAuth) {
      proxyLog.info("Loaded device identity:", _cachedAuth.identity.deviceId.slice(0, 12) + "…");
    } else {
      proxyLog.warn("No device identity found — gateway may reject connections");
    }
  }
  return _cachedAuth;
}

/**
 * Resolve the signature token the same way the gateway does:
 * auth.token ?? auth.deviceToken ?? auth.bootstrapToken ?? null
 */
function resolveSignatureToken(auth: Record<string, string> | undefined): string {
  return auth?.token ?? auth?.deviceToken ?? auth?.bootstrapToken ?? "";
}

/**
 * Build a v3 signature payload and sign it, returning the `device` object
 * ready to inject into a connect frame.
 */
function buildDeviceBlock(
  identity: DeviceIdentity,
  nonce: string,
  connectParams: Record<string, unknown>,
) {
  const signedAtMs = Date.now();
  const client = connectParams.client as Record<string, string> | undefined;
  const auth = connectParams.auth as Record<string, string> | undefined;
  const clientId = client?.id ?? "gateway-client";
  const clientMode = client?.mode ?? "backend";
  const role = (connectParams.role as string) ?? "operator";
  const scopes = Array.isArray(connectParams.scopes)
    ? (connectParams.scopes as string[]).join(",")
    : "operator.read,operator.write,operator.admin";
  const token = resolveSignatureToken(auth);
  const platform = (client?.platform ?? process.platform).trim().toLowerCase();
  const deviceFamily = (client?.deviceFamily ?? "").trim().toLowerCase();

  const payload = [
    "v3",
    identity.deviceId,
    clientId,
    clientMode,
    role,
    scopes,
    String(signedAtMs),
    token,
    nonce,
    platform,
    deviceFamily,
  ].join("|");

  return {
    id: identity.deviceId,
    publicKey: publicKeyRawBase64Url(identity.publicKeyPem),
    signature: signDevicePayload(identity.privateKeyPem, payload),
    signedAt: signedAtMs,
    nonce,
  };
}

// ── Proxy core ───────────────────────────────────────────

function isForwardableCloseCode(code: number) {
  return (
    code === 1000 ||
    (code >= 1001 && code <= 1014 && code !== 1004 && code !== 1005 && code !== 1006) ||
    (code >= 3000 && code <= 4999)
  );
}

function proxyWebSocket(clientWs: WebSocket, gatewayUrl: string) {
  const upstream = new WebSocket(gatewayUrl);
  const bufferedMessages: Array<{ data: RawData; isBinary: boolean }> = [];

  let challengeNonce: string | null = null;
  const deviceAuth = getDeviceAuth();

  const connectTimeout = setTimeout(() => {
    if (upstream.readyState === WebSocket.CONNECTING) {
      proxyLog.error("upstream connection timeout");
      bufferedMessages.length = 0;
      upstream.terminate();
      if (clientWs.readyState === WebSocket.OPEN) {
        clientWs.close(1011, "Gateway connection timeout");
      }
    }
  }, UPSTREAM_CONNECT_TIMEOUT_MS);

  upstream.on("open", () => {
    clearTimeout(connectTimeout);
    for (const message of bufferedMessages) {
      upstream.send(message.data, { binary: message.isBinary });
    }
    bufferedMessages.length = 0;
  });

  upstream.on("message", (data, isBinary) => {
    try {
      if (!isBinary && deviceAuth && !challengeNonce) {
        const text = data.toString();
        try {
          const frame = JSON.parse(text);
          if (frame.type === "event" && frame.event === "connect.challenge") {
            challengeNonce = frame.payload?.nonce ?? null;
          }
        } catch {}
      }
      if (clientWs.readyState === WebSocket.OPEN) {
        clientWs.send(data, { binary: isBinary });
      }
    } catch (err) {
      proxyLog.error("send to client failed:", (err as Error).message);
    }
  });

  upstream.on("close", (code, reason) => {
    if (clientWs.readyState === WebSocket.OPEN) {
      const textReason = reason.toString();
      if (isForwardableCloseCode(code)) {
        clientWs.close(code, textReason);
      } else {
        clientWs.close();
      }
    }
  });

  upstream.on("error", (err) => {
    proxyLog.error("upstream error:", err.message);
    if (clientWs.readyState === WebSocket.OPEN) {
      clientWs.close(1011, "Gateway connection error");
    }
  });

  clientWs.on("message", (data, isBinary) => {
    let payload = data;

    if (!isBinary && deviceAuth && challengeNonce) {
      try {
        const text = typeof data === "string" ? data : (data as Buffer).toString();
        const frame = JSON.parse(text);
        if (frame.type === "req" && frame.method === "connect" && frame.params) {
          if (!frame.params.auth) frame.params.auth = {};
          if (deviceAuth.operatorToken && !frame.params.auth.deviceToken) {
            frame.params.auth.deviceToken = deviceAuth.operatorToken;
          }
          if (frame.params.client) {
            frame.params.client.platform = process.platform;
          }
          frame.params.device = buildDeviceBlock(
            deviceAuth.identity,
            challengeNonce,
            frame.params,
          );
          payload = Buffer.from(JSON.stringify(frame));
          challengeNonce = null;
          proxyLog.info("Injected device identity into connect handshake");
        }
      } catch {}
    }

    if (upstream.readyState === WebSocket.OPEN) {
      upstream.send(payload, { binary: isBinary });
      return;
    }
    if (
      upstream.readyState === WebSocket.CONNECTING &&
      bufferedMessages.length < MAX_BUFFERED_MESSAGES
    ) {
      bufferedMessages.push({ data: payload as RawData, isBinary });
    }
  });

  clientWs.on("close", () => {
    clearTimeout(connectTimeout);
    bufferedMessages.length = 0;
    if (upstream.readyState === WebSocket.OPEN || upstream.readyState === WebSocket.CONNECTING) {
      upstream.close();
    }
  });

  clientWs.on("error", (err) => {
    proxyLog.error("client error:", err.message);
    if (upstream.readyState === WebSocket.OPEN) {
      upstream.close();
    }
  });
}

/** Validate WebSocket upgrade origin against host header. */
function checkOrigin(req: IncomingMessage, socket: Duplex): boolean {
  const origin = req.headers.origin;
  const host = req.headers.host;
  if (origin && host) {
    try {
      const originHost = new URL(origin).host;
      if (originHost !== host) {
        proxyLog.warn(`Rejected WS upgrade: origin ${origin} does not match host ${host}`);
        socket.write("HTTP/1.1 403 Forbidden\r\n\r\n");
        socket.destroy();
        return false;
      }
    } catch {
      proxyLog.warn(`Rejected WS upgrade: invalid origin ${origin}`);
      socket.write("HTTP/1.1 403 Forbidden\r\n\r\n");
      socket.destroy();
      return false;
    }
  }
  return true;
}

/**
 * Attach a WebSocket proxy to an HTTP server.
 * Intercepts upgrade requests to `path` and proxies them to `gatewayUrl`.
 */
export function attachWsProxy(
  server: import("http").Server,
  gatewayUrl: string,
  path = "/api/gateway",
) {
  const wss = new WebSocketServer({ noServer: true });

  server.on("upgrade", (req, socket, head) => {
    if (req.url === path) {
      if (!checkOrigin(req, socket)) return;
      wss.handleUpgrade(req, socket as Duplex, head, (clientWs) => {
        proxyWebSocket(clientWs, gatewayUrl);
      });
    }
  });

  wss.on("error", (err) => {
    proxyLog.error("server error:", err.message);
  });
}

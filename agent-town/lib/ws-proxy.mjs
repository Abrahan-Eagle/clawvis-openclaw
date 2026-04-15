/* Generated from lib/ws-proxy.ts — do not edit; run: pnpm build:ws-proxy */

// lib/ws-proxy.ts
import crypto from "crypto";
import fs from "fs";
import path from "path";
import { WebSocket, WebSocketServer } from "ws";

// lib/logger.ts
var isProd = typeof process !== "undefined" && process.env.NODE_ENV === "production";
function noop() {
}
function createLogger(tag) {
  const prefix = `[${tag}]`;
  if (isProd) {
    return {
      debug: noop,
      info: noop,
      warn: console.warn.bind(console, prefix),
      error: console.error.bind(console, prefix)
    };
  }
  return {
    debug: console.debug.bind(console, prefix),
    info: console.info.bind(console, prefix),
    warn: console.warn.bind(console, prefix),
    error: console.error.bind(console, prefix)
  };
}

// lib/ws-proxy.ts
var proxyLog = createLogger("WS Proxy");
var MAX_BUFFERED_MESSAGES = 100;
var UPSTREAM_CONNECT_TIMEOUT_MS = 15e3;
function base64UrlEncode(buf) {
  return buf.toString("base64").replaceAll("+", "-").replaceAll("/", "_").replace(/=+$/g, "");
}
function publicKeyRawBase64Url(pem) {
  const spki = crypto.createPublicKey(pem).export({ type: "spki", format: "der" });
  const ED25519_SPKI_PREFIX_LEN = 12;
  return base64UrlEncode(spki.subarray(ED25519_SPKI_PREFIX_LEN));
}
function signDevicePayload(privateKeyPem, payload) {
  const key = crypto.createPrivateKey(privateKeyPem);
  return base64UrlEncode(crypto.sign(null, Buffer.from(payload, "utf8"), key));
}
function loadDeviceAuth() {
  try {
    const stateDir = path.join(process.env.HOME ?? "", ".openclaw");
    const idRaw = fs.readFileSync(path.join(stateDir, "identity", "device.json"), "utf-8");
    const identity = JSON.parse(idRaw);
    if (!identity.deviceId || !identity.publicKeyPem || !identity.privateKeyPem) return null;
    let operatorToken = null;
    try {
      const authRaw = fs.readFileSync(path.join(stateDir, "identity", "device-auth.json"), "utf-8");
      const authData = JSON.parse(authRaw);
      operatorToken = authData.tokens?.operator?.token ?? null;
    } catch {
    }
    return { identity, operatorToken };
  } catch {
  }
  return null;
}
var _cachedAuth;
function getDeviceAuth() {
  if (_cachedAuth === void 0) {
    _cachedAuth = loadDeviceAuth();
    if (_cachedAuth) {
      proxyLog.info("Loaded device identity:", _cachedAuth.identity.deviceId.slice(0, 12) + "\u2026");
    } else {
      proxyLog.warn("No device identity found \u2014 gateway may reject connections");
    }
  }
  return _cachedAuth;
}
function resolveSignatureToken(auth) {
  return auth?.token ?? auth?.deviceToken ?? auth?.bootstrapToken ?? "";
}
function buildDeviceBlock(identity, nonce, connectParams) {
  const signedAtMs = Date.now();
  const client = connectParams.client;
  const auth = connectParams.auth;
  const clientId = client?.id ?? "gateway-client";
  const clientMode = client?.mode ?? "backend";
  const role = connectParams.role ?? "operator";
  const scopes = Array.isArray(connectParams.scopes) ? connectParams.scopes.join(",") : "operator.read,operator.write,operator.admin";
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
    deviceFamily
  ].join("|");
  return {
    id: identity.deviceId,
    publicKey: publicKeyRawBase64Url(identity.publicKeyPem),
    signature: signDevicePayload(identity.privateKeyPem, payload),
    signedAt: signedAtMs,
    nonce
  };
}
function isForwardableCloseCode(code) {
  return code === 1e3 || code >= 1001 && code <= 1014 && code !== 1004 && code !== 1005 && code !== 1006 || code >= 3e3 && code <= 4999;
}
function proxyWebSocket(clientWs, gatewayUrl) {
  const upstream = new WebSocket(gatewayUrl);
  const bufferedMessages = [];
  let challengeNonce = null;
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
        } catch {
        }
      }
      if (clientWs.readyState === WebSocket.OPEN) {
        clientWs.send(data, { binary: isBinary });
      }
    } catch (err) {
      proxyLog.error("send to client failed:", err.message);
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
        const text = typeof data === "string" ? data : data.toString();
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
            frame.params
          );
          payload = Buffer.from(JSON.stringify(frame));
          challengeNonce = null;
          proxyLog.info("Injected device identity into connect handshake");
        }
      } catch {
      }
    }
    if (upstream.readyState === WebSocket.OPEN) {
      upstream.send(payload, { binary: isBinary });
      return;
    }
    if (upstream.readyState === WebSocket.CONNECTING && bufferedMessages.length < MAX_BUFFERED_MESSAGES) {
      bufferedMessages.push({ data: payload, isBinary });
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
function checkOrigin(req, socket) {
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
function attachWsProxy(server, gatewayUrl, path2 = "/api/gateway") {
  const wss = new WebSocketServer({ noServer: true });
  server.on("upgrade", (req, socket, head) => {
    if (req.url === path2) {
      if (!checkOrigin(req, socket)) return;
      wss.handleUpgrade(req, socket, head, (clientWs) => {
        proxyWebSocket(clientWs, gatewayUrl);
      });
    }
  });
  wss.on("error", (err) => {
    proxyLog.error("server error:", err.message);
  });
}
export {
  attachWsProxy
};

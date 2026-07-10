/* Generated from lib/auggie-bridge.ts — do not edit; run: pnpm build:auggie-bridge */

// lib/auggie-bridge.ts
import { spawn } from "child_process";
import { writeFileSync, mkdirSync, unlinkSync } from "fs";
import { join } from "path";
import { tmpdir } from "os";
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

// lib/auggie-bridge.ts
var log = createLogger("Auggie Bridge");
var runCounter = 0;
var activeClientState = null;
var workerRoster = [];
function sendFrame(state, frame) {
  if (state.ws.readyState !== WebSocket.OPEN) return;
  try {
    state.ws.send(JSON.stringify(frame));
  } catch (err) {
    log.error("sendFrame failed:", err.message);
  }
}
function sendEvent(state, event, payload) {
  sendFrame(state, { type: "event", event, payload, seq: state.seq++ });
}
function sendResponse(state, id, ok, payloadOrError) {
  const frame = { type: "res", id, ok };
  if (ok) {
    frame.payload = payloadOrError;
  } else {
    frame.error = payloadOrError;
  }
  sendFrame(state, frame);
}
function parseAuggieOutput(raw) {
  const idx = raw.indexOf("{");
  if (idx === -1) return null;
  try {
    return JSON.parse(raw.slice(idx));
  } catch {
    const lines = raw.split("\n");
    for (let i = lines.length - 1; i >= 0; i--) {
      const line = lines[i].trim();
      if (line.startsWith("{")) {
        try {
          return JSON.parse(line);
        } catch {
          continue;
        }
      }
    }
    return null;
  }
}
function checkOrigin(req, socket) {
  const origin = req.headers.origin;
  const host = req.headers.host;
  if (origin && host) {
    try {
      const originHost = new URL(origin).host;
      if (originHost !== host) {
        log.warn(`Rejected WS upgrade: origin ${origin} does not match host ${host}`);
        socket.write("HTTP/1.1 403 Forbidden\r\n\r\n");
        socket.destroy();
        return false;
      }
    } catch {
      log.warn(`Rejected WS upgrade: invalid origin ${origin}`);
      socket.write("HTTP/1.1 403 Forbidden\r\n\r\n");
      socket.destroy();
      return false;
    }
  }
  return true;
}
function buildWorkerRosterContext(currentSeatLabel) {
  if (workerRoster.length <= 1) return "";
  const others = workerRoster.filter((w) => w.label !== currentSeatLabel);
  if (others.length === 0) return "";
  const lines = others.map(
    (w) => `  \u2022 seatId="${w.seatId}" \u2014 ${w.label} (${w.roleTitle ?? "Worker"})`
  );
  return "\n\nYou have team members available. Use the dispatch_to_worker tool to delegate tasks:\n" + lines.join("\n") + "\n";
}
function buildPersonalityPrefix(params) {
  const label = params.seatLabel;
  const role = params.seatRole;
  if (!label && !role) return "[You are powered by Auggie. Stay in character when responding.]\n\n";
  const parts = [];
  if (label) parts.push(`Your name is "${label}".`);
  if (role) parts.push(`Your role is ${role}.`);
  parts.push("Stay in character when responding.");
  const rosterCtx = buildWorkerRosterContext(label);
  return `[${parts.join(" ")}${rosterCtx}]

`;
}
function handleChatSend(state, id, params) {
  const sessionKey = params.sessionKey ?? "default";
  const rawMessage = params.message ?? "";
  const runId = `auggie_${Date.now()}_${++runCounter}`;
  const message = buildPersonalityPrefix(params) + rawMessage;
  sendResponse(state, id, true, { runId, status: "accepted" });
  sendEvent(state, "agent", { runId, sessionKey, stream: "lifecycle", data: { phase: "start" } });
  const args = ["--print", "--output-format", "json"];
  const mcpConfigPath2 = writeMcpConfig();
  if (mcpConfigPath2) {
    args.push("--mcp-config", mcpConfigPath2);
  }
  const existingSessionId = state.sessionMap.get(sessionKey);
  if (existingSessionId) {
    args.push("--resume", existingSessionId);
  }
  args.push("--");
  args.push(message);
  log.info(`Spawning auggie for run ${runId}:`, ["auggie", ...args].join(" "));
  const port = process.env.PORT ?? "3000";
  let child;
  try {
    child = spawn("auggie", args, {
      stdio: ["ignore", "pipe", "pipe"],
      env: {
        ...process.env,
        AGENT_TOWN_PORT: port,
        AGENT_TOWN_WORKERS: JSON.stringify(workerRoster),
        AGENT_TOWN_DISPATCH_SECRET: dispatchSecret
      }
    });
  } catch (err) {
    const errMsg = `Failed to spawn auggie: ${err.message}`;
    log.error(errMsg);
    sendEvent(state, "agent", {
      runId,
      sessionKey,
      stream: "lifecycle",
      data: { phase: "error", error: errMsg }
    });
    sendEvent(state, "chat", { runId, sessionKey, state: "error" });
    return;
  }
  state.runningProcesses.set(runId, child);
  let stdout = "";
  let stderr = "";
  child.stdout.on("data", (chunk) => {
    stdout += chunk.toString();
  });
  child.stderr.on("data", (chunk) => {
    stderr += chunk.toString();
  });
  child.on("error", (err) => {
    log.error(`auggie process error for run ${runId}:`, err.message);
    state.runningProcesses.delete(runId);
    sendEvent(state, "agent", {
      runId,
      sessionKey,
      stream: "lifecycle",
      data: { phase: "error", error: err.message }
    });
    sendEvent(state, "chat", { runId, sessionKey, state: "error" });
  });
  child.on("close", (code) => {
    state.runningProcesses.delete(runId);
    if (code === null || code !== 0) {
      const errMsg = stderr.trim() || `auggie exited with code ${code}`;
      log.error(`auggie failed for run ${runId}:`, errMsg);
      sendEvent(state, "agent", {
        runId,
        sessionKey,
        stream: "lifecycle",
        data: { phase: "error", error: errMsg }
      });
      sendEvent(state, "chat", { runId, sessionKey, state: "error" });
      return;
    }
    const parsed = parseAuggieOutput(stdout);
    if (!parsed) {
      log.error(`auggie produced unparseable output for run ${runId}:`, stdout.slice(0, 500));
      sendEvent(state, "agent", {
        runId,
        sessionKey,
        stream: "lifecycle",
        data: { phase: "error", error: "Failed to parse auggie output" }
      });
      sendEvent(state, "chat", { runId, sessionKey, state: "error" });
      return;
    }
    if (typeof parsed.session_id === "string") {
      state.sessionMap.set(sessionKey, parsed.session_id);
      log.debug(`Mapped sessionKey ${sessionKey} \u2192 auggie session ${parsed.session_id}`);
    }
    const responseText = typeof parsed.result === "string" ? parsed.result : typeof parsed.response === "string" ? parsed.response : JSON.stringify(parsed);
    sendEvent(state, "agent", {
      runId,
      sessionKey,
      stream: "lifecycle",
      data: { phase: "end" }
    });
    sendEvent(state, "chat", {
      runId,
      sessionKey,
      state: "final",
      message: { content: [{ type: "text", text: responseText }] }
    });
    log.info(`Run ${runId} completed successfully`);
  });
}
function handleChatAbort(state, id, params) {
  const runId = params.runId;
  const sessionKey = params.sessionKey ?? "default";
  if (runId && state.runningProcesses.has(runId)) {
    const child = state.runningProcesses.get(runId);
    child.kill("SIGTERM");
    state.runningProcesses.delete(runId);
    log.info(`Aborted run ${runId}`);
  }
  sendResponse(state, id, true, {});
  if (runId) {
    sendEvent(state, "chat", { runId, sessionKey, state: "aborted" });
  }
}
async function handleModelsList(state, id) {
  try {
    const result = await new Promise((resolve, reject) => {
      const child = spawn("auggie", ["model", "list", "--json"], {
        stdio: ["ignore", "pipe", "pipe"]
      });
      let out = "";
      child.stdout.on("data", (chunk) => {
        out += chunk.toString();
      });
      child.on("error", reject);
      child.on("close", (code) => {
        if (code === 0) resolve(out);
        else reject(new Error(`auggie model list exited with code ${code}`));
      });
      setTimeout(() => {
        child.kill();
        reject(new Error("timeout"));
      }, 1e4);
    });
    const parsed = parseAuggieOutput(result);
    if (parsed && Array.isArray(parsed.models)) {
      sendResponse(state, id, true, { models: parsed.models });
      return;
    }
    const idx = result.indexOf("[");
    if (idx !== -1) {
      try {
        const arr = JSON.parse(result.slice(idx));
        if (Array.isArray(arr)) {
          sendResponse(state, id, true, { models: arr });
          return;
        }
      } catch {
      }
    }
  } catch (err) {
    log.warn("Failed to list auggie models:", err.message);
  }
  sendResponse(state, id, true, {
    models: [{ id: "default", provider: "auggie", contextWindow: 128e3 }]
  });
}
function handleMessage(state, raw) {
  let frame;
  try {
    frame = JSON.parse(raw);
  } catch {
    log.warn("Received non-JSON message, ignoring");
    return;
  }
  if (frame.type !== "req") {
    log.debug("Ignoring non-request frame:", frame.type);
    return;
  }
  const { id, method, params } = frame;
  if (!id || !method) {
    log.warn("Request frame missing id or method");
    return;
  }
  log.debug(`Request: ${method} (id=${id})`);
  switch (method) {
    case "connect":
      sendResponse(state, id, true, {
        type: "hello-ok",
        scopes: ["operator.read", "operator.write"]
      });
      break;
    case "chat.send":
      handleChatSend(state, id, params ?? {});
      break;
    case "chat.abort":
      handleChatAbort(state, id, params ?? {});
      break;
    case "sessions.list":
      sendResponse(state, id, true, { sessions: [] });
      break;
    case "sessions.preview":
      sendResponse(state, id, true, { previews: [] });
      break;
    case "models.list":
      void handleModelsList(state, id);
      break;
    default:
      log.warn(`Unknown method: ${method}`);
      sendResponse(state, id, false, {
        code: "unknown_method",
        message: `Unknown method: ${method}`
      });
      break;
  }
}
var dispatchSecret = `at_${Date.now()}_${Math.random().toString(36).slice(2)}`;
var mcpConfigPath = null;
function getMcpServerPath() {
  return join(process.cwd(), "lib", "mcp", "agent-town-mcp.mjs");
}
function writeMcpConfig() {
  if (workerRoster.length <= 1) return null;
  if (mcpConfigPath) return mcpConfigPath;
  try {
    const config = {
      mcpServers: {
        "agent-town": {
          command: "node",
          args: [getMcpServerPath()]
        }
      }
    };
    const dir = join(tmpdir(), "agent-town-mcp");
    mkdirSync(dir, { recursive: true });
    const filePath = join(dir, `mcp-config-${process.pid}.json`);
    writeFileSync(filePath, JSON.stringify(config), "utf-8");
    mcpConfigPath = filePath;
    log.info(`MCP config written to ${filePath}`);
    return filePath;
  } catch (err) {
    log.warn("Failed to write MCP config:", err.message);
    return null;
  }
}
function cleanupMcpConfig() {
  if (mcpConfigPath) {
    try {
      unlinkSync(mcpConfigPath);
    } catch {
    }
    mcpConfigPath = null;
  }
}
function dispatchToWorker(seatId, task) {
  return new Promise((resolve) => {
    const state = activeClientState;
    const seat = workerRoster.find((w) => w.seatId === seatId);
    if (!state || state.ws.readyState !== WebSocket.OPEN) {
      resolve({ result: "", error: "No active WebSocket client" });
      return;
    }
    if (!seat) {
      resolve({ result: "", error: `Unknown seatId: ${seatId}` });
      return;
    }
    const runId = `auggie_sub_${Date.now()}_${++runCounter}`;
    const sessionKey = `subagent:dispatch:${seatId}:${runId}`;
    const prefix = buildPersonalityPrefix({
      seatLabel: seat.label,
      seatRole: seat.roleTitle
    });
    const message = prefix + task;
    sendEvent(state, "agent", {
      runId,
      sessionKey,
      stream: "lifecycle",
      data: { phase: "start", label: `${seat.label}: ${task.slice(0, 40)}`, seatId }
    });
    const args = ["--print", "--output-format", "json"];
    const seatSessionKey = `dispatch:${seatId}`;
    const existingSessionId = state.sessionMap.get(seatSessionKey);
    if (existingSessionId) {
      args.push("--resume", existingSessionId);
    }
    args.push("--");
    args.push(message);
    log.info(`Dispatching to ${seat.label} (${seatId}), run ${runId}`);
    let child;
    try {
      child = spawn("auggie", args, {
        stdio: ["ignore", "pipe", "pipe"],
        env: { ...process.env }
      });
    } catch (err) {
      const errMsg = `Failed to spawn auggie for dispatch: ${err.message}`;
      log.error(errMsg);
      sendEvent(state, "agent", {
        runId,
        sessionKey,
        stream: "lifecycle",
        data: { phase: "error", error: errMsg }
      });
      resolve({ result: "", error: errMsg });
      return;
    }
    let stdout = "";
    let stderr = "";
    child.stdout.on("data", (chunk) => {
      stdout += chunk.toString();
    });
    child.stderr.on("data", (chunk) => {
      stderr += chunk.toString();
    });
    child.on("error", (err) => {
      log.error(`dispatch process error for run ${runId}:`, err.message);
      sendEvent(state, "agent", {
        runId,
        sessionKey,
        stream: "lifecycle",
        data: { phase: "error", error: err.message }
      });
      resolve({ result: "", error: err.message });
    });
    child.on("close", (code) => {
      if (code !== 0) {
        const errMsg = stderr.trim() || `auggie exited with code ${code}`;
        log.error(`dispatch failed for run ${runId}:`, errMsg);
        sendEvent(state, "agent", {
          runId,
          sessionKey,
          stream: "lifecycle",
          data: { phase: "error", error: errMsg }
        });
        resolve({ result: "", error: errMsg });
        return;
      }
      const parsed = parseAuggieOutput(stdout);
      const responseText = parsed ? typeof parsed.result === "string" ? parsed.result : typeof parsed.response === "string" ? parsed.response : JSON.stringify(parsed) : stdout.trim();
      if (parsed && typeof parsed.session_id === "string") {
        state.sessionMap.set(seatSessionKey, parsed.session_id);
      }
      sendEvent(state, "agent", {
        runId,
        sessionKey,
        stream: "lifecycle",
        data: { phase: "end" }
      });
      sendEvent(state, "chat", {
        runId,
        sessionKey,
        state: "final",
        message: { content: [{ type: "text", text: responseText }] }
      });
      log.info(`Dispatch to ${seat.label} completed (run ${runId})`);
      resolve({ result: responseText });
    });
  });
}
function validateDispatchSecret(secret) {
  return secret === dispatchSecret;
}
function setWorkerRoster(seats) {
  workerRoster = seats;
  mcpConfigPath = null;
  log.debug(`Worker roster updated: ${seats.length} workers`);
}
function cleanupClient(state) {
  if (activeClientState === state) activeClientState = null;
  for (const [runId, child] of state.runningProcesses) {
    log.info(`Killing orphaned process for run ${runId}`);
    child.kill("SIGTERM");
  }
  state.runningProcesses.clear();
}
function attachAuggieBridge(server, path = "/api/gateway") {
  const wss = new WebSocketServer({ noServer: true });
  server.on("upgrade", (req, socket, head) => {
    if (req.url !== path) return;
    if (!checkOrigin(req, socket)) return;
    wss.handleUpgrade(req, socket, head, (ws) => {
      const state = {
        ws,
        seq: 0,
        runningProcesses: /* @__PURE__ */ new Map(),
        sessionMap: /* @__PURE__ */ new Map()
      };
      activeClientState = state;
      log.info("Client connected");
      sendEvent(state, "connect.challenge", {});
      ws.on("message", (data) => {
        handleMessage(state, data.toString());
      });
      ws.on("close", () => {
        log.info("Client disconnected");
        cleanupClient(state);
      });
      ws.on("error", (err) => {
        log.error("Client WS error:", err.message);
        cleanupClient(state);
      });
    });
  });
  wss.on("error", (err) => {
    log.error("WebSocketServer error:", err.message);
  });
  process.on("exit", cleanupMcpConfig);
  log.info(`Auggie bridge attached on ${path}`);
}
export {
  attachAuggieBridge,
  dispatchToWorker,
  setWorkerRoster,
  validateDispatchSecret
};

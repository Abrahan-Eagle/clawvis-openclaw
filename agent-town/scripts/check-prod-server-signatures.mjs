/**
 * Smoke-check: production attach* signatures match generated .mjs exports.
 * Run: node --input-type=module scripts/check-prod-server-signatures.mjs
 * (from agent-town/) — does not start Next or bind a port.
 */
import { createServer } from "node:http";
import { attachWsProxy } from "../lib/ws-proxy.mjs";
import { attachAuggieBridge } from "../lib/auggie-bridge.mjs";

const server = createServer();
let ok = true;

try {
  // New API: (server, gatewayUrl) — must not throw on attach
  attachWsProxy(server, "ws://127.0.0.1:18789/");
} catch (e) {
  console.error("FAIL attachWsProxy(server, url):", e);
  ok = false;
}

try {
  attachAuggieBridge(server);
} catch (e) {
  console.error("FAIL attachAuggieBridge(server):", e);
  ok = false;
}

// Old API would treat WebSocket constructor as gatewayUrl — detect arity mismatch
if (attachWsProxy.length < 2) {
  console.error("FAIL: attachWsProxy arity unexpected:", attachWsProxy.length);
  ok = false;
}

server.close();
if (!ok) process.exit(1);
console.log("OK: server.prod attach signatures match generated .mjs");

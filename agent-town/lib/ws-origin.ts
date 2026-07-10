/**
 * Pure origin checks for the WebSocket upgrade proxy.
 * Separated from ws-proxy.ts so Vitest can cover them without a live server.
 */

/**
 * Returns true if the Origin header is absent or matches the Host header.
 * When both are present and differ, the upgrade must be rejected (CSRF / cross-site WS).
 */
export function isAllowedWsOrigin(origin: string | undefined, host: string | undefined): boolean {
  if (!origin || !host) return true;
  try {
    const originHost = new URL(origin).host;
    return originHost === host;
  } catch {
    return false;
  }
}

/** Close codes safe to forward from upstream to the browser client. */
export function isForwardableCloseCode(code: number): boolean {
  return (
    code === 1000 ||
    (code >= 1001 && code <= 1014 && code !== 1004 && code !== 1005 && code !== 1006) ||
    (code >= 3000 && code <= 4999)
  );
}

/**
 * Path / agentId safety helpers for OpenClaw FS discovery.
 * Kept pure for unit tests (no Node FS I/O).
 */

import path from "node:path";

/** Ensure resolved target is within the allowed base directory. */
export function isSafePath(base: string, target: string): boolean {
  const resolvedBase = path.resolve(base);
  const resolved = path.resolve(target);
  return resolved === resolvedBase || resolved.startsWith(resolvedBase + path.sep);
}

/** Validate agentId: no path separators or traversal. */
export function isValidAgentId(id: string): boolean {
  return /^[a-zA-Z0-9_-]+$/.test(id) && !id.includes("..");
}

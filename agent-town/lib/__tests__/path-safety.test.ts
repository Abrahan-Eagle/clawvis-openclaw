import { describe, it, expect } from "vitest";
import { isSafePath, isValidAgentId } from "../path-safety";

describe("isValidAgentId", () => {
  it("accepts alphanumeric, underscore and hyphen", () => {
    expect(isValidAgentId("jarvis")).toBe(true);
    expect(isValidAgentId("jarvis-deep")).toBe(true);
    expect(isValidAgentId("agent_01")).toBe(true);
  });

  it("rejects path separators and traversal", () => {
    expect(isValidAgentId("../etc")).toBe(false);
    expect(isValidAgentId("foo/bar")).toBe(false);
    expect(isValidAgentId("foo\\bar")).toBe(false);
    expect(isValidAgentId("..")).toBe(false);
    expect(isValidAgentId("a..b")).toBe(false);
  });

  it("rejects empty and special characters", () => {
    expect(isValidAgentId("")).toBe(false);
    expect(isValidAgentId("jarvis!")).toBe(false);
    expect(isValidAgentId("jar vis")).toBe(false);
  });
});

describe("isSafePath", () => {
  const base = "/home/user/.openclaw/agents";

  it("allows the base itself and children", () => {
    expect(isSafePath(base, base)).toBe(true);
    expect(isSafePath(base, `${base}/jarvis`)).toBe(true);
    expect(isSafePath(base, `${base}/jarvis/workspace`)).toBe(true);
  });

  it("rejects siblings that only share a prefix", () => {
    expect(isSafePath(base, "/home/user/.openclaw/agents-evil")).toBe(false);
    expect(isSafePath(base, "/home/user/.openclaw/agents_backup")).toBe(false);
  });

  it("rejects path traversal outside base", () => {
    expect(isSafePath(base, `${base}/../identity`)).toBe(false);
    expect(isSafePath(base, `${base}/jarvis/../../.ssh`)).toBe(false);
    expect(isSafePath(base, "/etc/passwd")).toBe(false);
  });
});

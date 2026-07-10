import { describe, it, expect } from "vitest";
import { isAllowedWsOrigin, isForwardableCloseCode } from "../ws-origin";

describe("isAllowedWsOrigin", () => {
  it("allows missing origin or host (non-browser / same-host tooling)", () => {
    expect(isAllowedWsOrigin(undefined, "localhost:3000")).toBe(true);
    expect(isAllowedWsOrigin("http://localhost:3000", undefined)).toBe(true);
    expect(isAllowedWsOrigin(undefined, undefined)).toBe(true);
  });

  it("allows matching origin and host", () => {
    expect(isAllowedWsOrigin("http://localhost:3000", "localhost:3000")).toBe(true);
    expect(isAllowedWsOrigin("https://app.example.com", "app.example.com")).toBe(true);
  });

  it("rejects cross-origin upgrades", () => {
    expect(isAllowedWsOrigin("http://evil.example", "localhost:3000")).toBe(false);
    expect(isAllowedWsOrigin("http://localhost:3001", "localhost:3000")).toBe(false);
  });

  it("rejects invalid origin URLs", () => {
    expect(isAllowedWsOrigin("not-a-url", "localhost:3000")).toBe(false);
  });
});

describe("isForwardableCloseCode", () => {
  it("forwards normal closure and app codes", () => {
    expect(isForwardableCloseCode(1000)).toBe(true);
    expect(isForwardableCloseCode(1001)).toBe(true);
    expect(isForwardableCloseCode(3000)).toBe(true);
    expect(isForwardableCloseCode(4000)).toBe(true);
  });

  it("does not forward reserved / invalid codes", () => {
    expect(isForwardableCloseCode(1004)).toBe(false);
    expect(isForwardableCloseCode(1005)).toBe(false);
    expect(isForwardableCloseCode(1006)).toBe(false);
    expect(isForwardableCloseCode(0)).toBe(false);
    expect(isForwardableCloseCode(1015)).toBe(false);
  });
});

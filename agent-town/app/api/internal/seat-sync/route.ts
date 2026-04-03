/**
 * POST /api/internal/seat-sync
 *
 * Optional hook used when Agent Town runs in Auggie mode to sync seat roster to MCP.
 * In OpenClaw-only dev, the client still POSTs here; respond 204 to avoid console noise.
 */

import { NextResponse } from "next/server";

export async function POST() {
  return new NextResponse(null, { status: 204 });
}

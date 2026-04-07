/**
 * Opciones compartidas de lanzamiento Playwright para career-ops.
 *
 * Si `npx playwright install chromium` falla en tu SO, usa el Chrome instalado:
 *   export CAREER_OPS_PLAYWRIGHT_CHANNEL=chrome
 *
 * Valores admitidos: chrome, chrome-beta, chrome-dev, msedge, chromium
 * (mismos canales que expone Playwright).
 */
import { chromium } from 'playwright';

const ALLOWED_CHANNELS = new Set([
  'chrome',
  'chrome-beta',
  'chrome-dev',
  'msedge',
  'chromium',
]);

export function getLaunchOptions() {
  const raw = process.env.CAREER_OPS_PLAYWRIGHT_CHANNEL?.trim();
  if (raw && ALLOWED_CHANNELS.has(raw)) {
    return { headless: true, channel: raw };
  }
  return { headless: true };
}

export function getConfiguredChannel() {
  const raw = process.env.CAREER_OPS_PLAYWRIGHT_CHANNEL?.trim();
  return raw && ALLOWED_CHANNELS.has(raw) ? raw : null;
}

export async function launchChromium() {
  return chromium.launch(getLaunchOptions());
}

/**
 * Opciones compartidas de lanzamiento Playwright para career-ops.
 *
 * Prioridad: variable de entorno CAREER_OPS_PLAYWRIGHT_CHANNEL >
 *   archivo config/playwright.env (si existe) >
 *   Chromium empaquetado (npx playwright install chromium).
 *
 * Valores admitidos: chrome, chrome-beta, chrome-dev, msedge, chromium
 */
import { existsSync, readFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { chromium } from 'playwright';

const __dirname = dirname(fileURLToPath(import.meta.url));

const ALLOWED_CHANNELS = new Set([
  'chrome',
  'chrome-beta',
  'chrome-dev',
  'msedge',
  'chromium',
]);

let cachedChannelFromFile;

function loadChannelFromFile() {
  if (cachedChannelFromFile !== undefined) return cachedChannelFromFile;
  cachedChannelFromFile = null;
  try {
    const p = join(__dirname, 'config', 'playwright.env');
    if (!existsSync(p)) return null;
    const text = readFileSync(p, 'utf8');
    for (const line of text.split('\n')) {
      const t = line.trim();
      if (!t || t.startsWith('#')) continue;
      const m = t.match(/^CAREER_OPS_PLAYWRIGHT_CHANNEL\s*=\s*(.+)$/);
      if (m) {
        const v = m[1].trim().replace(/^["']|["']$/g, '');
        if (ALLOWED_CHANNELS.has(v)) cachedChannelFromFile = v;
        break;
      }
    }
  } catch {
    /* ignore */
  }
  return cachedChannelFromFile;
}

export function getConfiguredChannel() {
  const fromEnv = process.env.CAREER_OPS_PLAYWRIGHT_CHANNEL?.trim();
  if (fromEnv && ALLOWED_CHANNELS.has(fromEnv)) return fromEnv;
  const fromFile = loadChannelFromFile();
  return fromFile && ALLOWED_CHANNELS.has(fromFile) ? fromFile : null;
}

export function getLaunchOptions() {
  const ch = getConfiguredChannel();
  if (ch) return { headless: true, channel: ch };
  return { headless: true };
}

export async function launchChromium() {
  return chromium.launch(getLaunchOptions());
}

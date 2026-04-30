/**
 * JMC v1.11 — UI dashboard (vanilla JS; v1.9 base + omnibus observabilidad/UX)
 */
const LS_KEY = "jmc_bearer_token";
const LS_API_BASE = "jmc_api_base";
const LS_LAST_EXPORT = "jmc_last_export_at";
const LS_POLL = "jmc_poll_sec";
/** IDs de eventos de actividad marcados como leídos (centro de notificaciones). */
const LS_NOTIF_READ = "jmc_notif_read_ids";
const API_CACHE_MS = 5000;
/** Evita crecimiento ilimitado del caché GET (orden FIFO en Map). */
const API_CACHE_MAX = 100;
const apiCache = new Map();
/** IDs únicos para gradientes SVG en sparklines (evita colisiones en el DOM). */
let _sparkSeq = 0;
/** null = sin ping aún; true/false último resultado /v1/health */
let lastHealthOk = null;
/** null = desconocido; true/false según último GET /v1/modes/current (mode_write_enabled) */
let lastModeWriteEnabled = null;

/** Ventana horaria Gateway (1–168); persistido en localStorage. */
let gatewayWindowHours = 24;

let taskFilter = { status: "open", agent: "", q: "", tags: [] };
let actCursor = null;
let actFilters = { agent: "", kind: "", tag: "", since: "", limit: 80, group: "flat" };
/** Búsqueda en vista Modes (matriz). */
let modesQuery = "";
/** Filtro AG en vista Approvals (desde Gates). */
let apFilters = { ag: "" };
/** Filtros vista Automations (carpeta / trigger en keys YAML). */
let autoFilterFolder = "all";
let autoFilterTrigger = "all";
/** Última lista de tareas cargada (command palette / modales). */
let tasksCacheForPalette = [];
/** @type {"table"|"board"} */
let tasksViewMode = "table";
/** @type {"comfortable"|"compact"} */
let uiDensity = "comfortable";
let agentsSortKey = "id";
let agentsSortDir = "asc";
let agentsQuery = "";
/** Panel lateral de agentes en tablero: colapsado o no. */
let tasksBoardRailCollapsed = false;
/** Conversación activa en vista Chat (`/v1/chat/...`). */
let chatActiveConvId = "";

/** `agentId` → `{ emoji, color }` desde último fetch de `/v1/openclaw/agents` (openclaw.json). */
let agentUiById = {};
let memorySelectedPath = "";
let filesRoot = "docs";
let filesSelectedRel = "";

/** Último payload exportable por vista (clave = id de NAV). */
const viewExportPayload = {};

function loadPersistedFilters() {
  try {
    const o = window.jmcFilterStore ? window.jmcFilterStore.read() : {};
    if (!o || typeof o !== "object") return;
    if (o.taskFilter && typeof o.taskFilter === "object") {
      taskFilter = { status: "open", agent: "", q: "", tags: [], ...o.taskFilter };
      if (!Array.isArray(taskFilter.tags)) taskFilter.tags = [];
    }
    if (o.actFilters && typeof o.actFilters === "object") {
      actFilters = { agent: "", kind: "", tag: "", since: "", limit: 80, group: "flat", ...o.actFilters };
      actFilters.limit = Math.min(500, Math.max(10, parseInt(String(actFilters.limit), 10) || 80));
      if (!["flat", "by_task", "by_dossier"].includes(actFilters.group)) actFilters.group = "flat";
    }
    if (typeof o.modesQuery === "string") modesQuery = o.modesQuery;
    if (o.apFilters && typeof o.apFilters === "object") {
      apFilters = { ag: "", ...o.apFilters };
    }
    if (typeof o.autoFilterFolder === "string" && o.autoFilterFolder) autoFilterFolder = o.autoFilterFolder;
    if (o.autoFilterTrigger === "all" || o.autoFilterTrigger === "with" || o.autoFilterTrigger === "without") {
      autoFilterTrigger = o.autoFilterTrigger;
    }
    if (o.gatewayWindowHours != null) {
      const n = Number(o.gatewayWindowHours);
      if (Number.isFinite(n)) gatewayWindowHours = Math.max(1, Math.min(168, Math.round(n)));
    }
    if (o.tasksViewMode === "table" || o.tasksViewMode === "board") tasksViewMode = o.tasksViewMode;
    if (o.uiDensity === "compact" || o.uiDensity === "comfortable") uiDensity = o.uiDensity;
    if (typeof o.agentsSortKey === "string") agentsSortKey = o.agentsSortKey;
    if (o.agentsSortDir === "asc" || o.agentsSortDir === "desc") agentsSortDir = o.agentsSortDir;
    if (typeof o.agentsQuery === "string") agentsQuery = o.agentsQuery;
    if (typeof o.tasksBoardRailCollapsed === "boolean") tasksBoardRailCollapsed = o.tasksBoardRailCollapsed;
    if (typeof o.chatActiveConvId === "string") chatActiveConvId = o.chatActiveConvId;
  } catch (_) {}
}

function persistFilters() {
  try {
    if (window.jmcFilterStore) {
      window.jmcFilterStore.write({
        taskFilter,
        actFilters,
        gatewayWindowHours,
        tasksViewMode,
        uiDensity,
        agentsSortKey,
        agentsSortDir,
        agentsQuery,
        tasksBoardRailCollapsed,
        modesQuery,
        apFilters,
        autoFilterFolder,
        autoFilterTrigger,
        chatActiveConvId,
      });
    }
  } catch (_) {}
}

function applyUiDensity() {
  document.body.classList.toggle("jmc-density-compact", uiDensity === "compact");
}

/** Filtros que afectan al tablero pero no al chip de estado JMC. */
function taskBoardHasExtraFilters() {
  return !!(taskFilter.agent || (taskFilter.tags && taskFilter.tags.length) || (taskFilter.q && taskFilter.q.trim()));
}

async function openTaskModal(taskId) {
  const tid = String(taskId || "").trim();
  if (!tid) return;
  try {
    const det = await api("/v1/state/tasks/" + encodeURIComponent(tid), { bypassCache: true });
    const d = det.data || {};
    const evs = d.events || [];
    const ho = d.handoffs || [];
    showModal(`
            <h2 style="margin-top:0">Tarea ${escapeHtml(tid)}</h2>
            <p><button type="button" class="btn btn--primary" id="copy-task-json">Copiar JSON</button></p>
            <h3>Eventos (${evs.length})</h3>
            <div class="timeline timeline--modal">${evs.map((ev) => activityEventHtml(ev)).join("")}</div>
            <h3>Handoffs (${ho.length})</h3>
            <pre class="mono raw-block">${escapeHtml(JSON.stringify(ho, null, 2))}</pre>`);
    const cp = document.getElementById("copy-task-json");
    if (cp)
      cp.onclick = () => void copyTextCatch(JSON.stringify(d, null, 2), null);
  } catch (err) {
    alert(err.message);
  }
}

function eventMatchesTagFilter(ev, tag) {
  const t = String(tag || "").trim();
  if (!t) return true;
  const tags = ev.tags;
  if (Array.isArray(tags) && tags.map(String).some((x) => x.includes(t))) return true;
  try {
    const blob = JSON.stringify(ev).toLowerCase();
    return blob.includes(t.toLowerCase());
  } catch (_) {
    return false;
  }
}

function automationFolderKey(path) {
  const s = String(path || "");
  const m = s.match(/automations\/([^/]+)/i);
  return m ? m[1].toLowerCase() : "other";
}

function pathBasename(p) {
  const s = String(p || "").replace(/\\/g, "/");
  const i = s.lastIndexOf("/");
  return i >= 0 ? s.slice(i + 1) : s;
}

function updateExportHint() {
  const el = document.getElementById("export-hint");
  if (!el) return;
  const iso = localStorage.getItem(LS_LAST_EXPORT);
  const txt = iso ? "Último export: " + new Date(iso).toLocaleString() : "";
  el.textContent = txt;
  el.title = iso ? String(iso) : "";
}

function getExportMeta() {
  return {
    ui_version: "1.11",
    taskFilter: { ...taskFilter, tags: [...(taskFilter.tags || [])] },
    actFilters: { ...actFilters },
    gatewayWindowHours,
    tasksViewMode,
    uiDensity,
    agentsSortKey,
    agentsSortDir,
    agentsQuery,
    tasksBoardRailCollapsed,
    modesQuery,
    apFilters,
    autoFilterFolder,
    autoFilterTrigger,
    chatActiveConvId,
    last_export_at: localStorage.getItem(LS_LAST_EXPORT),
    api_base: getApiBase() || null,
  };
}

function downloadJson(filename, obj) {
  if (obj == null || typeof obj !== "object") {
    alert("Sin datos para exportar en esta vista.");
    return;
  }
  const blob = new Blob([JSON.stringify(obj, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1500);
}

function exportFilename(prefix) {
  const d = new Date();
  const iso = d.toISOString().slice(0, 19).replace(/[-:T]/g, "");
  return `${prefix}-${iso}.json`;
}

function setViewExport(payload) {
  viewExportPayload[currentView] = {
    view: currentView,
    exported_at: new Date().toISOString(),
    export_meta: getExportMeta(),
    ...payload,
  };
}

const NAV = [
  ["overview", "Overview", "M"],
  ["health_deep", "Health+", "✚"],
  ["errors", "Errors", "‼"],
  ["zombies", "Zombies", "Zz"],
  ["latency", "Latency", "⏱"],
  ["coverage", "Coverage", "☑"],
  ["costs_compare", "$Δ", "¢"],
  ["about", "About", "ⓘ"],
  ["dossiers", "Dossiers", "F"],
  ["agents", "Agents", "A"],
  ["hierarchy", "Jerarquía", "⊞"],
  ["tasks", "Tasks", "T"],
  ["costs", "Costs", "$"],
  ["modes", "Modes", "◐"],
  ["approvals", "Approvals", "P"],
  ["escalations", "Escalations", "!"],
  ["heartbeats", "Heartbeats", "♥"],
  ["gateway", "Gateway", "G"],
  ["system", "System", "§"],
  ["cron", "Cron", "⏱"],
  ["memory", "Memory", "◈"],
  ["files", "Files", "≡"],
  ["office", "Office", "⌂"],
  ["automations", "Automations", "⚙"],
  ["activity", "Activity", "◎"],
  ["chat", "Chat", "💬"],
  ["gates", "Gates", "‡"],
];

let pollTimer = null;
/** Evita solapar ticks de polling cuando un render async tarda más que el intervalo. */
let pollInFlight = false;
/** AbortController del tab activo (cancela fetch al cambiar vista). */
let abortCtl = new AbortController();
/** Se incrementa en cada cambio de pestaña; los debounces comprueban antes de re-renderizar. */
let uiRenderGen = 0;
let currentView = "overview";
/** Atajo vim-style: pulsar <kbd>g</kbd> y luego letra (no en inputs). */
let jmcAwaitG = false;
let jmcAwaitGTimer = null;

function getToken() {
  return localStorage.getItem(LS_KEY) || "";
}

/** Origen del adapter (p. ej. http://127.0.0.1:8765). Vacío = misma URL que esta página. */
function normalizeApiBaseUrl(raw) {
  let s = String(raw || "").trim();
  if (!s) return "";
  if (!/^https?:\/\//i.test(s)) s = "http://" + s;
  s = s.replace(/\/+$/, "");
  try {
    const u = new URL(s);
    if (u.protocol !== "http:" && u.protocol !== "https:") return null;
    return u.origin;
  } catch {
    return null;
  }
}

function getApiBase() {
  const stored = localStorage.getItem(LS_API_BASE);
  if (!stored) return "";
  const n = normalizeApiBaseUrl(stored);
  if (n === null) {
    localStorage.removeItem(LS_API_BASE);
    return "";
  }
  return n;
}

function apiHeaders() {
  const t = getToken();
  const h = { Accept: "application/json" };
  if (t) h.Authorization = "Bearer " + t;
  return h;
}

async function api(path, opts = {}) {
  const method = (opts.method || "GET").toUpperCase();
  const signal = opts.signal !== undefined ? opts.signal : abortCtl.signal;
  const bypass = opts.bypassCache;
  const base = getApiBase();
  const key = base + "\0" + path;
  const now = Date.now();
  if (method === "GET" && !bypass && !opts.skipCache) {
    const hit = apiCache.get(key);
    if (hit && now - hit.t < API_CACHE_MS) return hit.data;
  }
  const headers = { ...apiHeaders(), ...(opts.headers || {}) };
  const init = { method, headers, signal };
  if (opts.body != null && method !== "GET" && method !== "HEAD") {
    if (typeof FormData !== "undefined" && opts.body instanceof FormData) {
      init.body = opts.body;
      delete init.headers["Content-Type"];
      delete init.headers["content-type"];
    } else {
      init.body = typeof opts.body === "string" ? opts.body : JSON.stringify(opts.body);
      if (!headers["Content-Type"] && !headers["content-type"]) init.headers["Content-Type"] = "application/json";
    }
  }
  const r = await fetch(base + path, init);
  const text = await r.text();
  let j = {};
  if (text.trim()) {
    try {
      j = JSON.parse(text);
    } catch {
      if (!r.ok) throw new Error(text.trim().slice(0, 400) || r.statusText);
      throw new Error("Respuesta no JSON del adapter");
    }
  }
  if (!r.ok) {
    if (r.status === 401 && getToken()) {
      try {
        if (localStorage.getItem("jmc_api_ok")) {
          showToast("Bearer rechazado (401). Revise el token guardado.", "warn");
          localStorage.removeItem("jmc_api_ok");
        }
      } catch (_) {}
    }
    let msg = j.detail ?? j.error ?? r.statusText;
    if (typeof msg === "object") msg = JSON.stringify(msg);
    if (!msg || msg === r.statusText) {
      msg = text.trim().slice(0, 400) || r.statusText;
    }
    throw new Error(typeof msg === "string" ? msg : JSON.stringify(msg));
  }
  if (r.ok && getToken()) {
    try {
      localStorage.setItem("jmc_api_ok", "1");
    } catch (_) {}
  }
  if (method === "GET" && !bypass && !opts.skipCache) {
    apiCache.set(key, { t: now, data: j });
    while (apiCache.size > API_CACHE_MAX) {
      const k0 = apiCache.keys().next().value;
      if (k0 === undefined) break;
      apiCache.delete(k0);
    }
  }
  return j;
}

function errMessage(reason) {
  if (!reason) return "Error";
  return reason.message ? String(reason.message) : String(reason);
}

function showToast(msg, tone) {
  let el = document.getElementById("jmc-toast");
  if (!el) {
    el = document.createElement("div");
    el.id = "jmc-toast";
    el.setAttribute("role", "status");
    document.body.appendChild(el);
  }
  el.className = "jmc-toast" + (tone ? " jmc-toast--" + tone : " jmc-toast--info");
  el.textContent = msg;
  el.hidden = false;
  if (showToast._t) clearTimeout(showToast._t);
  showToast._t = setTimeout(() => {
    el.hidden = true;
  }, 3400);
}

function escapeHtml(s) {
  if (window.JMC_TABLES && window.JMC_TABLES.escapeHtml) return window.JMC_TABLES.escapeHtml(s);
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;")
    .replace(/`/g, "&#96;");
}

/** Resalta primera coincidencia de `q` en snippet (HTML escapado + &lt;mark&gt;). */
function snippetWithMark(snippet, q) {
  const s = String(snippet || "");
  const needle = String(q || "").trim();
  if (needle.length < 2) return escapeHtml(s.slice(0, 220));
  const low = s.toLowerCase();
  const idx = low.indexOf(needle.toLowerCase());
  if (idx < 0) return escapeHtml(s.slice(0, 220));
  const a = escapeHtml(s.slice(0, idx));
  const mid = escapeHtml(s.slice(idx, idx + needle.length));
  const b = escapeHtml(s.slice(idx + needle.length, 220));
  return `${a}<mark>${mid}</mark>${b}`;
}

function agentHashHue(id) {
  const s = String(id || "?");
  let h = 0;
  for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) | 0;
  return Math.abs(h) % 360;
}

/** Evita inyección CSS desde openclaw.json: sólo hex / rgb(a) / hsl(a). */
function sanitizeUiColor(raw) {
  const s = String(raw || "").trim();
  if (/^#[0-9a-fA-F]{3,8}$/.test(s)) return s;
  if (/^rgba?\([^)]+\)$/i.test(s)) return s;
  if (/^hsla?\([^)]+\)$/i.test(s)) return s;
  return "";
}

function agentAvatarHtml(agentId, ui, sizeClass) {
  const id = String(agentId || "?");
  const emojiRaw = ui && ui.emoji != null ? String(ui.emoji).trim().slice(0, 8) : "";
  const face = emojiRaw || id.slice(0, 2).toUpperCase();
  const safeColor = sanitizeUiColor(ui && ui.color);
  const bg = safeColor || `hsl(${agentHashHue(id)} 52% 40%)`;
  const sc = sizeClass ? " " + sizeClass : "";
  return `<span class="jmc-agent-avatar${sc}" style="--jmc-av-bg:${escapeHtml(bg)}" title="${escapeHtml(id)}"><span class="jmc-agent-avatar__face">${escapeHtml(face)}</span></span>`;
}

function rebuildAgentUiMap(list) {
  const next = {};
  for (const a of list || []) {
    const id = String(a.id || a.agentId || "").trim();
    if (!id) continue;
    const u = a.ui && typeof a.ui === "object" ? a.ui : {};
    if (u.emoji || u.color || u.description || u.location || u.birth_date) {
      next[id] = {
        emoji: u.emoji,
        color: u.color,
        description: u.description,
        location: u.location,
        birth_date: u.birth_date,
      };
    }
  }
  agentUiById = next;
}

function applyBrandFromHealth(brand) {
  if (!brand || typeof brand !== "object") return;
  const name = String(brand.name || "").trim() || "JMC";
  const emoji = String(brand.emoji || "").trim() || "◆";
  const company = String(brand.company || "").trim();
  const owner = String(brand.owner || "").trim();
  const subParts = [company, owner].filter(Boolean);
  const elLogo = document.getElementById("sidebar-brand-logo");
  const elName = document.getElementById("sidebar-brand-name");
  const elSub = document.getElementById("sidebar-brand-sub");
  if (elLogo) elLogo.textContent = emoji;
  if (elName) elName.textContent = name;
  if (elSub) {
    const desc = String(brand.description || "").trim();
    const loc = String(brand.location || "").trim();
    const bd = String(brand.birth_date || "").trim();
    const soc = String(brand.social || "").trim();
    const bits = [desc && desc.slice(0, 48), loc, bd, soc].filter(Boolean);
    elSub.textContent = bits.length ? bits.join(" · ") : "v1.10 · Jarvis Mission Control";
  }
  const extra = subParts.length ? ` · ${subParts.join(" · ")}` : "";
  document.title = `${name}${extra} — JMC`;
}

function notifEventKey(ev) {
  return `${ev.ts || ""}|${String(ev.type || "")}|${String(ev.agent || "")}|${String(ev.task_id || "")}`;
}

function loadNotifReadSet() {
  try {
    const a = JSON.parse(localStorage.getItem(LS_NOTIF_READ) || "[]");
    return new Set(Array.isArray(a) ? a : []);
  } catch {
    return new Set();
  }
}

function saveNotifReadSet(set) {
  const arr = [...set].slice(-200);
  try {
    localStorage.setItem(LS_NOTIF_READ, JSON.stringify(arr));
  } catch (_) {}
}

async function refreshAgentUiFromApi(signal) {
  if (!getToken()) return;
  try {
    const j = await api("/v1/openclaw/agents", { signal: signal ?? abortCtl.signal });
    const cfg = (j.data && j.data.config) || {};
    const list = (cfg.agents && cfg.agents.list) || [];
    rebuildAgentUiMap(list);
  } catch (_) {}
}

async function updateGlobalNotifBadge(signal) {
  const badge = document.getElementById("sidebar-global-badge");
  if (!badge) return;
  if (!getToken()) {
    badge.textContent = "";
    badge.classList.remove("sidebar-global-badge--on");
    badge.title = "";
    return;
  }
  try {
    const since = new Date(Date.now() - 86400000).toISOString();
    const [sumJ, actJ] = await Promise.all([
      api("/v1/state/summary", { signal: signal ?? abortCtl.signal, bypassCache: true }),
      api("/v1/state/activity?limit=300&since=" + encodeURIComponent(since), { signal: signal ?? abortCtl.signal, bypassCache: true }),
    ]);
    const read = loadNotifReadSet();
    const pa = sumJ && sumJ.data != null ? Number(sumJ.data.pending_approvals || 0) : 0;
    const wu = sumJ && sumJ.data != null ? Number(sumJ.data.waiting_user || 0) : 0;
    const evs = (actJ && actJ.data && actJ.data.events) || [];
    const warns = evs.filter((e) => {
      const t = String(e.type || "").toLowerCase();
      return t === "dossier-warn" || t === "block";
    });
    const unreadWarns = warns.filter((e) => !read.has(notifEventKey(e)));
    const n = pa + wu + unreadWarns.length;
    if (n > 0) {
      badge.textContent = n > 99 ? "99+" : String(n);
      badge.classList.add("sidebar-global-badge--on");
      badge.title = `Approvals ${pa}, escalaciones ${wu}, alertas actividad ${unreadWarns.length}`;
    } else {
      badge.textContent = "";
      badge.classList.remove("sidebar-global-badge--on");
      badge.title = "";
    }
  } catch {
    badge.textContent = "";
    badge.classList.remove("sidebar-global-badge--on");
    badge.title = "";
  }
}

function openNotificationsModal() {
  void (async () => {
    let pa = 0;
    let wu = 0;
    let warns = [];
    const since = new Date(Date.now() - 86400000).toISOString();
    try {
      const sumJ = await api("/v1/state/summary", { bypassCache: true });
      pa = Number(sumJ.data?.pending_approvals || 0);
      wu = Number(sumJ.data?.waiting_user || 0);
    } catch (_) {}
    try {
      const actJ = await api("/v1/state/activity?limit=300&since=" + encodeURIComponent(since), { bypassCache: true });
      const evs = actJ.data?.events || [];
      warns = evs.filter((e) => {
        const t = String(e.type || "").toLowerCase();
        return t === "dossier-warn" || t === "block";
      });
    } catch (_) {}
    const read = loadNotifReadSet();
    warns.forEach((e) => read.add(notifEventKey(e)));
    saveNotifReadSet(read);
    void updateGlobalNotifBadge(abortCtl.signal);
    const warnLines = warns
      .slice(0, 18)
      .map((e) => `<li><span class="mono">${escapeHtml(e.ts || "")}</span> ${badgeEv(e.type)} ${escapeHtml(String(e.agent || ""))}</li>`)
      .join("");
    showModal(`<h2 style="margin-top:0">Notificaciones</h2>
      <p class="muted" style="font-size:0.88rem">Centro cliente: contador = approvals + escalaciones + alertas de actividad no leídas (<span class="mono">dossier-warn</span> / <span class="mono">block</span>, 24h). Al abrir este panel, las alertas listadas se marcan leídas.</p>
      <ul style="text-align:left;font-size:0.9rem;padding-left:1.1rem">
        <li><strong>Approvals pendientes:</strong> ${pa} — <button type="button" class="btn-link-quiet" id="notif-go-ap">Ir a Approvals</button></li>
        <li><strong>Escalaciones (waiting user):</strong> ${wu} — <button type="button" class="btn-link-quiet" id="notif-go-es">Ir a Escalations</button></li>
        <li><strong>Activity:</strong> <button type="button" class="btn-link-quiet" id="notif-go-act">Ir a Activity</button></li>
      </ul>
      <h3 style="font-size:0.95rem">Últimas alertas (24h)</h3>
      <ul style="font-size:0.82rem;text-align:left;margin:0;padding-left:1.1rem;max-height:14rem;overflow:auto">${warnLines || '<li class="muted">Ninguna en la ventana.</li>'}</ul>`);
    const go = (id) => {
      hideModal();
      activateTab(id);
    };
    document.getElementById("notif-go-ap").onclick = () => go("approvals");
    document.getElementById("notif-go-es").onclick = () => go("escalations");
    document.getElementById("notif-go-act").onclick = () => go("activity");
  })();
}

function searchGlobalClose() {
  const bd = document.getElementById("search-backdrop");
  if (bd) bd.hidden = true;
}

function searchGlobalOpen() {
  const bd = document.getElementById("search-backdrop");
  const inp = document.getElementById("search-global-input");
  const list = document.getElementById("search-global-list");
  if (!bd || !inp || !list) return;
  bd.hidden = false;
  inp.value = "";
  list.innerHTML = '<li class="muted" style="padding:0.5rem 0.75rem">Escribe al menos 2 caracteres</li>';
  inp.focus();
}

let searchGlobalTimer;
/** Cancela búsquedas globales obsoletas (tecleo rápido). */
let searchGlobalAbort = null;
let searchGlobalReq = 0;

/** Vistas que el poll periódico puede repintar sin perder foco en formularios. */
const POLL_AUTO_REFRESH_VIEWS = new Set([
  "overview",
  "health_deep",
  "errors",
  "zombies",
  "latency",
  "coverage",
  "about",
]);

function searchGlobalRun(q) {
  const list = document.getElementById("search-global-list");
  if (!list) return;
  const qq = String(q || "").trim();
  if (qq.length < 2) {
    list.innerHTML = '<li class="muted" style="padding:0.5rem 0.75rem">Mínimo 2 caracteres</li>';
    return;
  }
  if (searchGlobalAbort) searchGlobalAbort.abort();
  searchGlobalAbort = new AbortController();
  const myReq = ++searchGlobalReq;
  const sig = searchGlobalAbort.signal;
  list.innerHTML = '<li class="muted" style="padding:0.5rem 0.75rem">Buscando…</li>';
  void api("/v1/search/?q=" + encodeURIComponent(qq), { bypassCache: true, signal: sig })
    .then((j) => {
      if (myReq !== searchGlobalReq) return;
      const hits = (j.data && j.data.hits) || [];
      if (!hits.length) {
        list.innerHTML = '<li class="muted" style="padding:0.5rem 0.75rem">Sin resultados</li>';
        return;
      }
      list.innerHTML = hits
        .map(
          (h) =>
            `<li><button type="button" class="cmdk-item" style="white-space:normal;text-align:left" data-rel="${escapeHtml(h.rel_path || "")}" data-line="${escapeHtml(String(h.line || ""))}"><span class="mono">${escapeHtml(h.rel_path || "")}</span> :${escapeHtml(String(h.line || ""))}<br/><span class="muted" style="font-size:0.78rem">${snippetWithMark(h.snippet || "", qq)}</span></button></li>`
        )
        .join("");
      list.querySelectorAll(".cmdk-item").forEach((btn) => {
        btn.onclick = () => {
          const rel = btn.getAttribute("data-rel") || "";
          showToast(rel + (btn.getAttribute("data-line") ? " L" + btn.getAttribute("data-line") : ""));
          searchGlobalClose();
        };
      });
    })
    .catch((e) => {
      if (e && e.name === "AbortError") return;
      if (myReq !== searchGlobalReq) return;
      list.innerHTML = `<li class="muted" style="padding:0.5rem 0.75rem">${escapeHtml(errMessage(e))}</li>`;
    });
}

function fmtRel(ts) {
  if (!ts) return "—";
  const t = Date.parse(ts);
  if (Number.isNaN(t)) return escapeHtml(String(ts));
  const sec = Math.round((Date.now() - t) / 1000);
  if (sec < 60) return "hace " + sec + "s";
  if (sec < 3600) return "hace " + Math.round(sec / 60) + "m";
  if (sec < 86400) return "hace " + Math.round(sec / 3600) + "h";
  return "hace " + Math.round(sec / 86400) + "d";
}

function copyText(text) {
  const t = String(text);
  if (navigator.clipboard && navigator.clipboard.writeText) {
    return navigator.clipboard.writeText(t);
  }
  const ta = document.createElement("textarea");
  ta.value = t;
  document.body.appendChild(ta);
  ta.select();
  document.execCommand("copy");
  document.body.removeChild(ta);
  return Promise.resolve();
}

/** Copia al portapapeles con toast de éxito o aviso si falla (p. ej. permisos). */
function copyTextCatch(text, okMsg) {
  return copyText(text)
    .then(() => {
      if (okMsg) showToast(okMsg, "ok");
    })
    .catch(() => showToast("No se pudo copiar al portapapeles.", "warn"));
}

function _renderCatch(p) {
  if (p && typeof p.then === "function") {
    void p.catch((e) => {
      if (e && e.name === "AbortError") return;
      showToast(errMessage(e), "warn");
    });
  }
}

function badgeTask(row) {
  const js = row.jmc_status || "";
  let cls = "badge--open";
  let lab = js || row.status || "?";
  if (js === "waiting_for_user" || row.status === "blocked") {
    cls = "badge--wait";
    lab = "wait";
  } else if (js === "closed" || row.status === "done") {
    cls = "badge--closed";
    lab = "closed";
  } else {
    lab = "open";
  }
  return `<span class="badge ${cls}">${escapeHtml(lab)}</span>`;
}

function badgeMode(m) {
  const x = String(m || "?").toUpperCase();
  const map = { D: "badge--mode-d", C: "badge--mode-c", B: "badge--mode-b", A: "badge--mode-a" };
  return `<span class="badge ${map[x] || "badge--mode-d"}">${escapeHtml(x)}</span>`;
}

function matrixCellClass(txt) {
  const s = String(txt).toLowerCase();
  if (s.includes("siempre ceo")) return "mat-siempre";
  if (s.includes("escala")) return "mat-escala";
  if (s.startsWith("solo")) return "mat-solo";
  return "";
}

function badgeEvClass(typ) {
  const s = String(typ || "event").toLowerCase();
  const map = {
    start: "badge-ev--start",
    end: "badge-ev--end",
    handoff: "badge-ev--handoff",
    "dossier-warn": "badge-ev--warn",
    block: "badge-ev--block",
    resume: "badge-ev--resume",
    event: "badge-ev--event",
  };
  return map[s] || "badge-ev--default";
}

function badgeEv(typ) {
  const lab = typ || "—";
  return `<span class="badge-ev ${badgeEvClass(typ)}">${escapeHtml(lab)}</span>`;
}

function activityPayloadSummary(ev) {
  const p = ev.payload || {};
  const parts = [];
  if (p.note != null && p.note !== "") parts.push("note: " + String(p.note).slice(0, 120));
  if (p.task_id) parts.push("task: " + p.task_id);
  if (p.kind) parts.push("kind: " + p.kind);
  if (p.handoff_id) parts.push("handoff: " + p.handoff_id);
  if (p.Title) parts.push("title: " + String(p.Title).slice(0, 80));
  return parts.join(" · ") || "—";
}

function activityEventHtml(ev) {
  const raw = JSON.stringify(ev.payload || {}, null, 2);
  const tsDisp = fmtRel(ev.ts) || escapeHtml(String(ev.ts || ""));
  return `<div class="tl-item">
    <div class="tl-row1">
      <span class="tl-ts">${tsDisp}</span>
      <span class="tl-agent mono">${escapeHtml(ev.agent || "")}</span>
      ${badgeEv(ev.type)}
    </div>
    <div class="tl-summary muted">${escapeHtml(activityPayloadSummary(ev))}</div>
    <details class="tl-raw"><summary>Payload JSON</summary><pre class="tl-pre mono">${escapeHtml(raw)}</pre></details>
  </div>`;
}

function sparklineSVG(points, w = 400, h = 80) {
  if (!points.length) return '<p class="muted">Sin datos</p>';
  const pts2 = points.length < 2 ? [0, ...points] : points;
  const max = Math.max(...pts2, 1);
  const step = w / Math.max(pts2.length - 1, 1);
  const pad = 4;
  const pts = pts2.map((v, i) => {
    const x = pad + i * step;
    const y = pad + (h - 2 * pad) * (1 - v / max);
    return x + "," + y;
  });
  const polyPoints = pts.join(" ");
  const gid = "sg-" + ++_sparkSeq;
  return `<svg viewBox="0 0 ${w} ${h}" preserveAspectRatio="none" class="spark-svg"><defs><linearGradient id="${gid}" x1="0" x2="0" y1="0" y2="1"><stop offset="0%" stop-color="rgba(61,139,253,0.6)"/><stop offset="100%" stop-color="rgba(61,139,253,0)"/></linearGradient></defs><polyline fill="none" stroke="#3d8bfd" stroke-width="2" points="${polyPoints}"/><polygon fill="url(#${gid})" points="0,${h} ${polyPoints} ${w},${h}"/></svg>`;
}

function openclawModelString(raw) {
  if (raw == null || raw === "") return "";
  if (typeof raw === "object") {
    const p = raw.primary || raw.name;
    if (p) return String(p);
    const firstStr = Object.values(raw).find((v) => typeof v === "string");
    return firstStr ? String(firstStr) : "";
  }
  return String(raw);
}

/**
 * Muestra HTML en el modal (asigna innerHTML).
 * @param {string} html Fragmento ya escapado / seguro por el caller (p. ej. vía escapeHtml); no pasar datos crudos de usuario sin sanitizar.
 */
function showModal(html) {
  document.getElementById("modal-body").innerHTML = html;
  document.getElementById("modal-backdrop").hidden = false;
}

function hideModal() {
  document.getElementById("modal-backdrop").hidden = true;
}

function stalledTasks(tasks) {
  const day = 24 * 60 * 60 * 1000;
  const now = Date.now();
  return (tasks || []).filter((t) => {
    const st = t.jmc_status || "";
    const raw = t.status || "";
    if (st !== "open" && raw !== "in_progress") return false;
    const s = t.started_at;
    if (!s) return false;
    const ts = Date.parse(s);
    if (Number.isNaN(ts)) return false;
    return now - ts > day;
  });
}

function fmtDurMs(ms) {
  if (ms == null || Number.isNaN(ms)) return "—";
  const sec = Math.round(ms / 1000);
  if (sec < 120) return sec + "s";
  if (sec < 7200) return Math.round(sec / 60) + "m";
  if (sec < 172800) return Math.round(sec / 3600) + "h";
  return Math.round(sec / 86400) + "d";
}

function taskDurationMs(row) {
  const s = row.started_at;
  if (!s) return null;
  const a = Date.parse(s);
  if (Number.isNaN(a)) return null;
  const end = row.ended_at ? Date.parse(row.ended_at) : Date.now();
  if (Number.isNaN(end)) return null;
  return end - a;
}

/** task_id -> primer AG pendiente (desde /v1/state/pending_approvals). */
function pendingAgByTask(items) {
  const m = {};
  (items || []).forEach((it) => {
    const tid = String(it.task_id || it.taskId || "").trim();
    if (!tid || m[tid]) return;
    if (it.ag) m[tid] = String(it.ag);
  });
  return m;
}

function tagHue(str) {
  let h = 0;
  const s = String(str);
  for (let i = 0; i < s.length; i++) h = ((h << 5) - h + s.charCodeAt(i)) >>> 0;
  return h % 360;
}

function taskTagCountsMap(allTasks) {
  const m = {};
  for (const r of allTasks) {
    const tags = Array.isArray(r.tags) ? r.tags.map(String) : [];
    for (const t of tags) m[t] = (m[t] || 0) + 1;
  }
  return m;
}

function groupRowsByJmcStatus(rows) {
  const g = { open: [], waiting_for_user: [], closed: [] };
  for (const r of rows) {
    const js = r.jmc_status || "open";
    if (g[js]) g[js].push(r);
    else g.open.push(r);
  }
  return g;
}

/** Último ts por task_id y tareas con evento block/error/fail reciente (<24h). */
function buildActivityIndexesFromEvents(events, nowMs) {
  const lastTsByTask = new Map();
  const blockedRecentByTask = new Set();
  const MS_24H = 86400000;
  for (const ev of events || []) {
    const tid = ev.task_id;
    if (!tid) continue;
    const ts = Date.parse(ev.ts || "");
    if (Number.isNaN(ts)) continue;
    const tidStr = String(tid);
    const prev = lastTsByTask.get(tidStr);
    if (prev == null || ts > prev) lastTsByTask.set(tidStr, ts);
    const typ = String(ev.type || "").toLowerCase();
    if (nowMs - ts <= MS_24H && (typ.includes("block") || typ.includes("error") || typ.includes("fail"))) {
      blockedRecentByTask.add(tidStr);
    }
  }
  return { lastTsByTask, blockedRecentByTask };
}

/**
 * Columna del tablero MC-like (solo lectura; no modifica state).
 * Precedencia: done → review (wait o AG) → blocked → inbox / in_progress.
 */
function deriveBoardColumn(task, agMap, lastTsByTask, blockedRecentByTask, nowMs) {
  const tid = String(task.id || "");
  const js = task.jmc_status || "open";
  const hasAg = tid && !!agMap[tid];
  const lastAct = lastTsByTask.get(tid);
  const MS_24H = 86400000;
  const last24h = lastAct != null && nowMs - lastAct < MS_24H;
  const explicitBlocked = !!task.blocked || String(task.status || "").toLowerCase() === "blocked";
  const blockedRecent = tid && blockedRecentByTask.has(tid);

  if (js === "waiting_for_user") return "review";
  if (hasAg) return "review";
  if (js === "closed") return "done";
  if (explicitBlocked || blockedRecent) return "blocked";
  if (!last24h) return "inbox";
  return "in_progress";
}

function groupTasksByBoardCol(rows, agMap, idx, nowMs) {
  const cols = { inbox: [], in_progress: [], review: [], blocked: [], done: [] };
  for (const r of rows) {
    const col = deriveBoardColumn(r, agMap, idx.lastTsByTask, idx.blockedRecentByTask, nowMs);
    cols[col].push(r);
  }
  return cols;
}

/** Conteos open / wait / closed por owner (toda la lista de tareas del API). */
function agentsRailCountsFromTasks(allTasks) {
  const m = new Map();
  for (const t of allTasks) {
    const o = String(t.owner || "").trim() || "—";
    if (!m.has(o)) m.set(o, { open: 0, wait: 0, closed: 0 });
    const c = m.get(o);
    const js = t.jmc_status || "open";
    if (js === "closed") c.closed++;
    else if (js === "waiting_for_user") c.wait++;
    else c.open++;
  }
  return m;
}

function activityFeedLine(ev) {
  const sum = activityPayloadSummary(ev);
  const ag = String(ev.agent || "").trim();
  const av = ag ? agentAvatarHtml(ag, agentUiById[ag]) : "";
  return `<div class="feed-line feed-line--click" role="link" tabindex="0" data-feed-agent="${escapeHtml(ag)}">
    <span class="feed-line-ts muted">${fmtRel(ev.ts) || "—"}</span>
    ${badgeEv(ev.type)}
    ${av}<span class="mono">${escapeHtml(ev.agent || "")}</span>
    <span class="muted">${escapeHtml(sum.slice(0, 140))}${sum.length > 140 ? "…" : ""}</span>
  </div>`;
}

async function renderDossiers(root, signal) {
  root.innerHTML = `<p class="muted">Cargando…</p>`;
  try {
    const j = await api("/v1/dossiers", { signal });
    const items = (j.data && j.data.items) || [];
    if (!items.length) {
      root.innerHTML = `<h1 class="panel-title">Dossiers</h1><p class="muted">Sin entradas cli-*.json ni carpetas cli-* en client-dossiers.</p>`;
      setViewExport({ items: [] });
      return;
    }
    const dossierRows = items.map((it) => {
      const id = it.id || "";
      const brief = JSON.stringify(it.data || {}).slice(0, 120);
      return {
        id,
        file: it.file || "",
        brief: `${brief}…`,
        _did: id,
      };
    });
    const dossierTable = window.JMC_TABLES.renderDataTable(
      [
        { key: "id", label: "ID" },
        { key: "file", label: "Archivo" },
        { key: "brief", label: "Resumen" },
      ],
      dossierRows,
      {
        rowClass: () => "click-row dossier-row",
        rowAttrs: (row) => ({ "data-dossier": row._did || row.id || "" }),
      }
    );
    root.innerHTML = `
      <h1 class="panel-title">Dossiers</h1>
      <p class="muted" style="margin-top:0">Click en una fila para ver tareas, handoffs y eventos agregados.</p>
      ${dossierTable}`;
    root.querySelectorAll(".dossier-row").forEach((tr) => {
      tr.onclick = async () => {
        const did = tr.getAttribute("data-dossier");
        if (!did) return;
        try {
          const det = await api("/v1/state/dossier/" + encodeURIComponent(did), { bypassCache: true });
          const d = det.data || {};
          const tasks = d.tasks || [];
          const hands = d.handoffs || [];
          const evs = d.events || [];
          const met = d.metrics || {};
          showModal(`
            <h2 style="margin-top:0">Dossier <span class="mono">${escapeHtml(did)}</span></h2>
            <div class="tab-bar" role="tablist">
              <button type="button" class="tab-btn active" data-tab="t1">Tareas (${tasks.length})</button>
              <button type="button" class="tab-btn" data-tab="t2">Handoffs (${hands.length})</button>
              <button type="button" class="tab-btn" data-tab="t3">Eventos (${evs.length})</button>
              <button type="button" class="tab-btn" data-tab="t4">Métricas</button>
            </div>
            <div class="tab-panel active" data-panel="t1">
              <pre class="mono raw-block">${escapeHtml(JSON.stringify(tasks, null, 2))}</pre>
            </div>
            <div class="tab-panel" data-panel="t2" hidden>
              <pre class="mono raw-block">${escapeHtml(JSON.stringify(hands, null, 2))}</pre>
            </div>
            <div class="tab-panel" data-panel="t3" hidden>
              <div class="timeline timeline--modal">${evs.map((ev) => activityEventHtml(ev)).join("") || '<p class="muted">Sin eventos.</p>'}</div>
            </div>
            <div class="tab-panel" data-panel="t4" hidden>
              <ul style="font-size:0.9rem">
                <li>tasks_open: <strong>${escapeHtml(String(met.tasks_open ?? "—"))}</strong></li>
                <li>tasks_closed: <strong>${escapeHtml(String(met.tasks_closed ?? "—"))}</strong></li>
                <li>handoffs_pending: <strong>${escapeHtml(String(met.handoffs_pending ?? "—"))}</strong></li>
                <li>last_event_ts: <span class="mono">${escapeHtml(String(met.last_event_ts || "—"))}</span></li>
              </ul>
            </div>`);
          const modal = document.getElementById("modal-body");
          modal.querySelectorAll(".tab-btn").forEach((btn) => {
            btn.onclick = () => {
              const id = btn.getAttribute("data-tab");
              modal.querySelectorAll(".tab-btn").forEach((b) => b.classList.toggle("active", b === btn));
              modal.querySelectorAll(".tab-panel").forEach((p) => {
                p.hidden = p.getAttribute("data-panel") !== id;
                p.classList.toggle("active", p.getAttribute("data-panel") === id);
              });
            };
          });
        } catch (err) {
          alert(err.message);
        }
      };
    });
    setViewExport({ items });
  } catch (e) {
    root.innerHTML = `<p class="err">${escapeHtml(e.message)}</p>`;
  }
}

async function renderApprovals(root, signal) {
  root.innerHTML = `<p class="muted">Cargando…</p>`;
  try {
    const j = await api("/v1/state/pending_approvals", { signal });
    let items = (j.data && j.data.items) || [];
    const agF = String(apFilters.ag || "").trim();
    if (agF) items = items.filter((it) => String(it.ag || "") === agF);
    if (!items.length) {
      root.innerHTML = `<h1 class="panel-title">Approvals</h1><p class="muted">${
        agF ? `Ningún pendiente para <span class="mono">${escapeHtml(agF)}</span>.` : `Sin handoffs con <span class="mono">approval.status=pending</span>.`
      }</p>${agF ? `<p><button type="button" class="btn btn--ghost" id="ap-clear-filter">Quitar filtro AG</button></p>` : ""}`;
      const clr = root.querySelector("#ap-clear-filter");
      if (clr)
        clr.onclick = () => {
          apFilters.ag = "";
          persistFilters();
          renderApprovals(root, abortCtl.signal);
        };
      setViewExport({ items: [] });
      return;
    }
    root.innerHTML =
      `<h1 class="panel-title">Approvals pendientes</h1>
      <p class="muted" style="margin-top:0">AG / canales / schema (solo lectura).${agF ? ` Filtro: <span class="mono">${escapeHtml(agF)}</span> <button type="button" class="btn btn--ghost" id="ap-clear-filter" style="font-size:0.78rem">Quitar</button>` : ""}</p>` +
      items
        .map(
          (it, i) =>
            `<div class="esc-card">
            <div style="display:flex;justify-content:space-between;align-items:start;gap:0.5rem;flex-wrap:wrap">
              <div>
                <span class="badge-ag">${escapeHtml(it.ag || "AG?")}</span>
                <span class="mono" style="margin-left:0.35rem">${escapeHtml(it.schema || "")}</span>
                <span class="muted"> · dossier <span class="mono">${escapeHtml(it.dossier_id || "—")}</span></span>
              </div>
              <div style="display:flex;gap:0.35rem;flex-wrap:wrap">
              <button type="button" class="btn btn--ghost btn-open-task-ap" data-task-id="${escapeHtml(String(it.task_id || ""))}">Abrir tarea</button>
              <button type="button" class="btn btn--primary btn-copy-ap" data-idx="${i}">Copiar payload JSON</button>
              </div>
            </div>
            <p style="margin:0.35rem 0 0;font-size:0.85rem">task <span class="mono">${escapeHtml(it.task_id || "")}</span></p>
            <p class="muted" style="margin:0.25rem 0 0;font-size:0.82rem">channels: ${escapeHtml((it.channels || []).join(", ") || "—")}</p>
          </div>`
        )
        .join("");
    root.querySelectorAll(".btn-copy-ap").forEach((btn) => {
      btn.onclick = () => {
        const i = Number(btn.getAttribute("data-idx"));
        void copyTextCatch(JSON.stringify(items[i], null, 2), null);
      };
    });
    root.querySelectorAll(".btn-open-task-ap").forEach((btn) => {
      btn.onclick = () => openTaskModal(btn.getAttribute("data-task-id"));
    });
    const clr2 = root.querySelector("#ap-clear-filter");
    if (clr2)
      clr2.onclick = () => {
        apFilters.ag = "";
        persistFilters();
        renderApprovals(root, abortCtl.signal);
      };
    setViewExport({ items, apFilters });
  } catch (e) {
    root.innerHTML = `<p class="err">${escapeHtml(e.message)}</p>`;
  }
}

async function renderHeartbeats(root, signal) {
  root.innerHTML = `<p class="muted">Cargando…</p>`;
  try {
    const settled = await Promise.allSettled([api("/v1/openclaw/heartbeats", { signal }), api("/v1/openclaw/agents", { signal })]);
    const hbJ = settled[0].status === "fulfilled" ? settled[0].value : null;
    const agJ = settled[1].status === "fulfilled" ? settled[1].value : null;
    const hbItems = (hbJ && hbJ.data && hbJ.data.items) || [];
    const cfgList = (agJ && agJ.data && agJ.data.config && agJ.data.config.agents && agJ.data.config.agents.list) || [];
    const hbById = new Map(hbItems.map((it) => [String(it.id || ""), it]));
    let bodyRows = "";
    if (cfgList.length) {
      rebuildAgentUiMap(cfgList);
      bodyRows = cfgList
        .map((a) => {
          const id = String(a.id || a.agentId || "?");
          const av = agentAvatarHtml(id, a.ui || agentUiById[id]);
          const hb = hbById.get(id);
          if (hb) {
            const ah = hb.activeHours || {};
            const win = `${ah.start || "—"}–${ah.end || "—"} ${escapeHtml(ah.timezone || "")}`;
            const ok = hb.within_active_hours;
            const cls = ok ? "hb-on" : "hb-off";
            return `<tr><td class="mono" style="white-space:nowrap">${av}${escapeHtml(id)}</td><td>${escapeHtml(hb.every || "—")}</td><td><span class="${cls}">${escapeHtml(win)}</span></td><td class="mono" style="font-size:0.8rem">${escapeHtml(hb.next_due_estimate || "—")}</td><td>${escapeHtml(String(hb.target ?? "—"))}</td></tr>`;
          }
          return `<tr><td class="mono" style="white-space:nowrap">${av}${escapeHtml(id)}</td><td><span class="badge badge--wait">sin heartbeat configurado</span></td><td class="muted">—</td><td class="muted">—</td><td class="muted">—</td></tr>`;
        })
        .join("");
    } else if (hbItems.length) {
      bodyRows = hbItems
        .map((it) => {
          const id = String(it.id || "?");
          const av = agentAvatarHtml(id, agentUiById[id]);
          const ah = it.activeHours || {};
          const win = `${ah.start || "—"}–${ah.end || "—"} ${escapeHtml(ah.timezone || "")}`;
          const ok = it.within_active_hours;
          const cls = ok ? "hb-on" : "hb-off";
          return `<tr><td class="mono" style="white-space:nowrap">${av}${escapeHtml(id)}</td><td>${escapeHtml(it.every || "—")}</td><td><span class="${cls}">${escapeHtml(win)}</span></td><td class="mono" style="font-size:0.8rem">${escapeHtml(it.next_due_estimate || "—")}</td><td>${escapeHtml(String(it.target ?? "—"))}</td></tr>`;
        })
        .join("");
    }
    root.innerHTML = `
      <h1 class="panel-title">Heartbeats</h1>
      <p class="muted" style="margin-top:0">Desde <span class="mono">openclaw.json</span> → <span class="mono">agents.list[].heartbeat</span>. Se listan todos los agentes declarados en <span class="mono">agents.list</span>.</p>
      ${
        bodyRows
          ? `<table class="data"><thead><tr><th>Agente</th><th>every</th><th>Ventana activa</th><th>Próximo (est.)</th><th>target</th></tr></thead><tbody>${bodyRows}</tbody></table>`
          : '<p class="muted">Sin agentes en <span class="mono">agents.list</span> y sin entradas de heartbeat.</p>'
      }`;
    setViewExport({ items: hbItems, agents_list_count: cfgList.length });
  } catch (e) {
    root.innerHTML = `<p class="err">${escapeHtml(e.message)}</p>`;
  }
}

async function renderAutomations(root, signal) {
  root.innerHTML = `<p class="muted">Cargando…</p>`;
  try {
    const j = await api("/v1/openclaw/automations", { signal });
    const d = j.data || {};
    const sync = d.sync_check || {};
    const prev = d.yaml_preview || {};
    const files = d.files || [];
    const nested = d.nested || [];
    const uniqPaths = [...new Set(Object.keys(prev).filter((k) => k !== "__truncated__"))].sort();
    const folderOpts = ["all", "jarvis", "marketing", "ventas", "registry", "shared", "other"];
    const folderChips = folderOpts
      .map(
        (f) =>
          `<button type="button" class="chip ${autoFilterFolder === f ? "active" : ""}" data-auto-folder="${f}">${escapeHtml(f === "all" ? "Todas las carpetas" : f)}</button>`
      )
      .join("");
    const trigChips = ["all", "with", "without"]
      .map(
        (t) =>
          `<button type="button" class="chip ${autoFilterTrigger === t ? "active" : ""}" data-auto-trigger="${t}">${escapeHtml(t === "all" ? "Trigger: todos" : t === "with" ? "Con trigger" : "Sin trigger")}</button>`
      )
      .join("");
    const filteredPaths = uniqPaths.filter((path) => {
      const fk = automationFolderKey(path);
      const folderOk = autoFilterFolder === "all" || fk === autoFilterFolder || (autoFilterFolder === "other" && !folderOpts.slice(1, -1).includes(fk));
      if (!folderOk) return false;
      const ent = prev[path] || {};
      const keysArr = Array.isArray(ent.keys) ? ent.keys.map(String) : [];
      const hasTrig = keysArr.some((k) => k.toLowerCase() === "trigger");
      if (autoFilterTrigger === "with" && !hasTrig) return false;
      if (autoFilterTrigger === "without" && hasTrig) return false;
      return true;
    });
    const byBase = new Map();
    for (const path of filteredPaths) {
      const bn = pathBasename(path).toLowerCase();
      if (!byBase.has(bn)) byBase.set(bn, []);
      byBase.get(bn).push(path);
    }
    let dupRowCount = 0;
    for (const arr of byBase.values()) {
      if (arr.length > 1) dupRowCount += arr.length;
    }
    const autoSummary =
      filteredPaths.length > 0
        ? `<p class="muted" style="margin:0 0 0.5rem;font-size:0.82rem"><strong>${filteredPaths.length}</strong> rutas${
            dupRowCount ? ` · <span class="auto-dup-warn">${dupRowCount} con basename duplicado</span>` : ""
          }</p>`
        : "";
    const rows = filteredPaths
      .map((path) => {
        const ent = prev[path];
        const keys = Array.isArray(ent.keys) ? ent.keys.join(", ") : JSON.stringify(ent);
        const bn = pathBasename(path).toLowerCase();
        const siblings = byBase.get(bn) || [];
        const isDup = siblings.length > 1;
        const tip = isDup ? siblings.filter((p) => p !== path).join("\n") : "";
        const dupBadge = isDup
          ? ` <span class="badge badge--wait auto-dup-badge" title="${escapeHtml(tip)}">duplicado</span>`
          : "";
        const loc = path.includes("/") ? "nested" : "raíz";
        return `<tr><td class="mono" style="font-size:0.78rem">${escapeHtml(path)}${dupBadge}</td><td>${escapeHtml(loc)}</td><td style="font-size:0.82rem">${escapeHtml(keys)}</td></tr>`;
      })
      .join("");
    root.innerHTML = `
      <h1 class="panel-title">Automations</h1>
      <p class="muted" style="margin-top:0">YAML en <span class="mono">automations/</span> · sync check</p>
      <p style="font-size:0.85rem">sync: <span class="mono">${sync.ok ? "OK" : "fail"}</span> ${sync.exit_code != null ? `(exit ${escapeHtml(String(sync.exit_code))})` : ""}</p>
      <p class="muted" style="font-size:0.8rem">Raíz: ${files.map((f) => `<span class="mono">${escapeHtml(f)}</span>`).join(", ") || "—"} · nested: ${nested.length}</p>
      <div class="toolbar" style="flex-wrap:wrap"><span class="muted" style="font-size:0.82rem">Carpeta:</span> ${folderChips}</div>
      <div class="toolbar" style="flex-wrap:wrap"><span class="muted" style="font-size:0.82rem">YAML:</span> ${trigChips}</div>
      ${autoSummary}
      <table class="data"><thead><tr><th>Ruta</th><th>Ubicación</th><th>keys / tipo</th></tr></thead><tbody>
      ${rows || '<tr><td colspan="3" class="muted">Sin previews o ningún archivo con los filtros.</td></tr>'}
      </tbody></table>`;
    root.querySelectorAll("[data-auto-folder]").forEach((b) => {
      b.onclick = () => {
        autoFilterFolder = b.getAttribute("data-auto-folder") || "all";
        persistFilters();
        renderAutomations(root, abortCtl.signal);
      };
    });
    root.querySelectorAll("[data-auto-trigger]").forEach((b) => {
      b.onclick = () => {
        autoFilterTrigger = b.getAttribute("data-auto-trigger") || "all";
        persistFilters();
        renderAutomations(root, abortCtl.signal);
      };
    });
    setViewExport(d);
  } catch (e) {
    root.innerHTML = `<p class="err">${escapeHtml(e.message)}</p>`;
  }
}

async function renderSystem(root, signal) {
  root.innerHTML = `<p class="muted">Cargando…</p>`;
  try {
    const j = await api("/v1/system/metrics", { signal });
    const d = j.data || {};
    const disks = (d.disk || []).slice(0, 8);
    const cpu = Number(d.cpu_percent);
    const memPct = d.mem && d.mem.percent != null ? Number(d.mem.percent) : NaN;
    const sparkPts = [cpu, memPct].every((n) => Number.isFinite(n)) ? [cpu, memPct] : [0, 0];
    root.innerHTML = `
      <h1 class="panel-title">System</h1>
      <p class="muted" style="margin-top:0">Snapshot local (<span class="mono">psutil</span>), caché ~2s en el adapter.</p>
      <div class="grid-dashboard">
        <div class="stat-card"><div class="stat-label">CPU %</div><div class="stat-val">${escapeHtml(String(d.cpu_percent ?? "—"))}</div></div>
        <div class="stat-card"><div class="stat-label">RAM %</div><div class="stat-val">${escapeHtml(String(d.mem?.percent ?? "—"))}</div></div>
        <div class="stat-card"><div class="stat-label">Uptime (s)</div><div class="stat-val">${escapeHtml(String(d.uptime_sec ?? "—"))}</div></div>
      </div>
      <div class="card-block" style="margin-top:1rem">
        <h3 style="margin-top:0;font-size:1rem">CPU / RAM (último snapshot)</h3>
        <div class="spark-wrap">${sparklineSVG(sparkPts)}</div>
      </div>
      <div class="card-block" style="margin-top:1rem">
        <h3 style="margin-top:0;font-size:1rem">Discos</h3>
        <table class="data"><thead><tr><th>Montaje</th><th>%</th><th>Usado / Total</th></tr></thead><tbody>
        ${disks.length ? disks.map((x) => `<tr><td class="mono">${escapeHtml(x.mountpoint || "")}</td><td>${escapeHtml(String(x.percent ?? "—"))}</td><td class="muted">${escapeHtml(String(x.used ?? ""))} / ${escapeHtml(String(x.total ?? ""))}</td></tr>`).join("") : '<tr><td colspan="3" class="muted">Sin particiones legibles</td></tr>'}
        </tbody></table>
      </div>
      <p class="muted" style="font-size:0.8rem">Red bytes: ↑ <span class="mono">${escapeHtml(String(d.net?.bytes_sent ?? "—"))}</span> · ↓ <span class="mono">${escapeHtml(String(d.net?.bytes_recv ?? "—"))}</span> · load: <span class="mono">${escapeHtml(JSON.stringify(d.load_avg || []))}</span></p>`;
    setViewExport(d);
  } catch (e) {
    root.innerHTML = `<p class="err">${escapeHtml(e.message)}</p>`;
  }
}

async function renderCron(root, signal) {
  root.innerHTML = `<p class="muted">Cargando…</p>`;
  try {
    const j = await api("/v1/openclaw/cron-timeline?days=7", { signal });
    const d = j.data || {};
    const agents = d.agents || [];
    const runs = d.runs_recent || [];
    const blocks = agents
      .map((ag) => {
        const id = escapeHtml(ag.id || "?");
        const mask = ag.hours_active || [];
        const cells = mask.map((on) => `<span class="cron-hour-cell${on ? " cron-hour-cell--on" : ""}"></span>`).join("");
        return `<div class="cron-agent-block"><h3 class="cron-agent-title">${id}</h3><div class="cron-hour-row">${cells}</div><p class="muted" style="font-size:0.72rem;margin:0">${mask.length} h · ventana ${escapeHtml(String(d.window_days || 7))} días (UTC)</p></div>`;
      })
      .join("");
    root.innerHTML = `
      <h1 class="panel-title">Cron</h1>
      <p class="muted" style="margin-top:0">Grilla horaria de <strong>ventanas activas</strong> por agente (heartbeats). Cada celda ≈ 1 h (izq. → más antiguo).</p>
      ${blocks || '<p class="muted">Sin agentes con heartbeat.</p>'}
      <div class="card-block" style="margin-top:1.5rem">
        <h3 style="margin-top:0;font-size:1rem">Heartbeats recientes (activity-log)</h3>
        <ul style="font-size:0.82rem;margin:0;padding-left:1.1rem;max-height:16rem;overflow:auto">${
          runs.length
            ? [...runs].reverse().slice(0, 24).map((r) => `<li><span class="mono">${escapeHtml(r.ts || "")}</span> · ${escapeHtml(r.agent || "")}</li>`).join("")
            : '<li class="muted">Sin heartbeats en el log reciente.</li>'
        }</ul>
      </div>`;
    setViewExport(d);
  } catch (e) {
    root.innerHTML = `<p class="err">${escapeHtml(e.message)}</p>`;
  }
}

async function renderMemory(root, signal) {
  root.innerHTML = `<p class="muted">Cargando…</p>`;
  try {
    const j = await api("/v1/memory/list", { signal });
    const items = (j.data && j.data.items) || [];
    const left = items
      .map((it) => {
        const rp = it.rel_path || "";
        const active = memorySelectedPath === rp ? " active" : "";
        const st = it.stale ? ` <span class="badge badge--wait" title="mtime &gt; ${it.stale_after_days || 14}d">stale</span>` : "";
        return `<button type="button" class="mem-item${active}" data-mem-path="${escapeHtml(rp)}">${escapeHtml(rp)} <span class="muted">(${escapeHtml(String(it.agent || ""))})</span>${st}</button>`;
      })
      .join("");
    let right = '<p class="muted">Selecciona un archivo.</p>';
    if (memorySelectedPath) {
      try {
        const fj = await api("/v1/memory/file?path=" + encodeURIComponent(memorySelectedPath), { signal });
        const fd = fj.data || {};
        if (fd.error === "too_large") right = `<p class="err">too_large</p>`;
        else right = `<pre class="mono memory-viewer">${escapeHtml(fd.content || "")}</pre>`;
      } catch (e) {
        right = `<p class="err">${escapeHtml(e.message)}</p>`;
      }
    }
    root.innerHTML = `
      <h1 class="panel-title">Memory / Soul</h1>
      <p class="muted" style="margin-top:0">Solo lectura · <span class="mono">agents/*/MEMORY.md</span> y <span class="mono">SOUL.md</span>.</p>
      <div class="memory-split">
        <div class="memory-list" id="mem-list-col">${left || '<p class="muted" style="padding:0.5rem">Sin archivos.</p>'}</div>
        <div id="mem-view-col">${right}</div>
      </div>`;
    root.querySelectorAll("[data-mem-path]").forEach((btn) => {
      btn.onclick = () => {
        memorySelectedPath = btn.getAttribute("data-mem-path") || "";
        renderMemory(root, abortCtl.signal);
      };
    });
    setViewExport({ items, selected: memorySelectedPath });
  } catch (e) {
    root.innerHTML = `<p class="err">${escapeHtml(e.message)}</p>`;
  }
}

async function renderFiles(root, signal) {
  root.innerHTML = `<p class="muted">Cargando…</p>`;
  try {
    const treeJ = await api("/v1/files/tree?root=" + encodeURIComponent(filesRoot), { signal });
    const entries = (treeJ.data && treeJ.data.entries) || [];
    const filesOnly = entries.filter((e) => e.type === "file");
    const list = filesOnly
      .map((e) => {
        const p = e.path || "";
        const act = filesSelectedRel === p ? " active" : "";
        return `<button type="button" class="mem-item${act}" data-files-path="${escapeHtml(p)}">${escapeHtml(p)}</button>`;
      })
      .join("");
    let right = '<p class="muted">Selecciona un fichero.</p>';
    if (filesSelectedRel) {
      try {
        const gj = await api(
          "/v1/files/get?root=" + encodeURIComponent(filesRoot) + "&path=" + encodeURIComponent(filesSelectedRel),
          { signal }
        );
        const gd = gj.data || {};
        if (gd.error === "too_large") right = `<p class="err">too_large</p>`;
        else right = `<pre class="mono memory-viewer">${escapeHtml(gd.content || "")}</pre>`;
      } catch (e) {
        right = `<p class="err">${escapeHtml(e.message)}</p>`;
      }
    }
    root.innerHTML = `
      <h1 class="panel-title">Files</h1>
      <p class="muted" style="margin-top:0">Solo lectura bajo raíces <span class="mono">docs</span>, <span class="mono">skills</span>, <span class="mono">automations</span>.</p>
      <div class="toolbar" style="flex-wrap:wrap">
        ${["docs", "skills", "automations"]
          .map((r) => `<button type="button" class="chip ${filesRoot === r ? "active" : ""}" data-files-root="${r}">${escapeHtml(r)}</button>`)
          .join("")}
      </div>
      <div class="memory-split">
        <div class="memory-list">${list || '<p class="muted" style="padding:0.5rem">Sin ficheros.</p>'}</div>
        <div>${right}</div>
      </div>`;
    root.querySelectorAll("[data-files-root]").forEach((b) => {
      b.onclick = () => {
        filesRoot = b.getAttribute("data-files-root") || "docs";
        filesSelectedRel = "";
        renderFiles(root, abortCtl.signal);
      };
    });
    root.querySelectorAll("[data-files-path]").forEach((btn) => {
      btn.onclick = () => {
        filesSelectedRel = btn.getAttribute("data-files-path") || "";
        renderFiles(root, abortCtl.signal);
      };
    });
    setViewExport({ root: filesRoot, file_count: filesOnly.length, selected: filesSelectedRel });
  } catch (e) {
    root.innerHTML = `<p class="err">${escapeHtml(e.message)}</p>`;
  }
}

async function renderOffice(root, signal) {
  root.innerHTML = `<p class="muted">Cargando…</p>`;
  try {
    const [agJ, gwJ] = await Promise.all([
      api("/v1/openclaw/agents", { signal }),
      api("/v1/openclaw/gateway?window_hours=24", { signal }).catch(() => ({ data: { agents: [] } })),
    ]);
    const cfg = (agJ.data && agJ.data.config) || {};
    const list = (cfg.agents && cfg.agents.list) || [];
    rebuildAgentUiMap(list);
    const gwAgents = (gwJ.data && gwJ.data.agents) || [];
    const silent = new Set(gwAgents.filter((x) => x.silent).map((x) => String(x.id)));
    const cards = list
      .map((a) => {
        const id = String(a.id || a.agentId || "?");
        const ui = a.ui || agentUiById[id] || {};
        const st = silent.has(id)
          ? `<span class="badge badge--wait">silent</span>`
          : `<span class="badge badge--closed">alive</span>`;
        return `<div class="office-card">
          ${agentAvatarHtml(id, ui, "jmc-agent-avatar--lg")}
          <div class="mono" style="font-weight:700">${escapeHtml(id)}</div>
          <div style="margin-top:0.35rem">${st}</div>
        </div>`;
      })
      .join("");
    root.innerHTML = `
      <h1 class="panel-title">Office</h1>
      <p class="muted" style="margin-top:0">Rejilla read-only: metadatos <span class="mono">ui.emoji</span> / <span class="mono">ui.color</span> + estado Gateway (24h).</p>
      <div class="office-grid">${cards || '<p class="muted">Sin agentes declarados.</p>'}</div>`;
    setViewExport({ agents: list.length, gateway_agents: gwAgents.length });
  } catch (e) {
    root.innerHTML = `<p class="err">${escapeHtml(e.message)}</p>`;
  }
}

/** --- JMC v1.10 (omnibus) vistas y utilidades --- */
async function renderHealthDeep(root, signal) {
  root.innerHTML = `<p class="muted">Cargando…</p>`;
  try {
    const j = await api("/v1/health/deep", { signal });
    const d = j.data || {};
    setViewExport(d);
    root.innerHTML = `<h1 class="panel-title">Health (deep)</h1>
      <p class="muted" style="margin-top:0">Agregado read-only: openclaw.json, activity, tasks, sync automations.</p>
      <pre class="mono raw-block" style="max-height:70vh;overflow:auto">${escapeHtml(JSON.stringify(d, null, 2))}</pre>
      <p class="toolbar"><button type="button" class="btn btn--ghost" id="hd-copy">Copiar JSON</button></p>`;
    const cp = root.querySelector("#hd-copy");
    if (cp) cp.onclick = () => void copyTextCatch(JSON.stringify(d, null, 2), "Copiado.");
  } catch (e) {
    root.innerHTML = `<p class="err">${escapeHtml(e.message)}</p>`;
  }
}

async function renderErrors(root, signal) {
  root.innerHTML = `<p class="muted">Cargando…</p>`;
  try {
    const j = await api("/v1/state/activity?limit=300", { signal });
    const evs = (j.data && j.data.events) || [];
    const bad = (t) => {
      const x = String(t || "").toLowerCase();
      return x === "block" || x === "dossier-warn" || x === "error" || x === "fail" || x.includes("error") || x.includes("fail");
    };
    const rows = evs.filter((e) => bad(e.type));
    setViewExport({ count: rows.length, sample: rows.slice(0, 50) });
    root.innerHTML = `<h1 class="panel-title">Errors / Warnings</h1>
      <p class="muted" style="margin-top:0">Filtrado cliente sobre <span class="mono">/v1/state/activity</span> (últimos 300).</p>
      <p><strong>${rows.length}</strong> eventos</p>
      <div class="overview-feed" role="feed">${rows.length ? rows.map((ev) => activityFeedLine(ev)).join("") : '<p class="muted">Ninguno en la ventana.</p>'}</div>`;
    root.querySelectorAll(".feed-line--click").forEach((el) => {
      el.onclick = () => {
        actFilters.agent = el.getAttribute("data-feed-agent") || "";
        persistFilters();
        activateTab("activity");
      };
    });
  } catch (e) {
    root.innerHTML = `<p class="err">${escapeHtml(e.message)}</p>`;
  }
}

async function renderZombies(root, signal) {
  root.innerHTML = `<p class="muted">Cargando…</p>`;
  try {
    const j = await api("/v1/state/zombies", { signal });
    const d = j.data || {};
    const items = d.items || [];
    setViewExport(d);
    root.innerHTML = `<h1 class="panel-title">Zombies</h1>
      <p class="muted" style="margin-top:0">Tareas <strong>open</strong> sin eventos recientes (umbral <span class="mono">${escapeHtml(String(d.threshold_hours ?? ""))}h</span> vía <span class="mono">JMC_TASK_ZOMBIE_HOURS</span>).</p>
      <p><strong>${d.count ?? items.length}</strong> ítems</p>
      <table class="data"><thead><tr><th>task_id</th><th>reason</th><th>owner</th><th>last_event</th></tr></thead><tbody>
      ${items.length ? items.map((z) => `<tr><td class="mono">${escapeHtml(z.task_id || "")}</td><td>${escapeHtml(z.reason || "")}</td><td>${escapeHtml(z.owner || "")}</td><td class="mono">${escapeHtml(z.last_event_ts || "—")}</td></tr>`).join("") : '<tr><td colspan="4" class="muted">Ninguno</td></tr>'}
      </tbody></table>`;
  } catch (e) {
    root.innerHTML = `<p class="err">${escapeHtml(e.message)}</p>`;
  }
}

async function renderLatency(root, signal) {
  root.innerHTML = `<p class="muted">Cargando…</p>`;
  try {
    const j = await api("/v1/state/latency", { signal });
    const d = j.data || {};
    setViewExport(d);
    const ag = (d.by_agent || []).slice(0, 25);
    const doss = (d.by_dossier || []).slice(0, 25);
    root.innerHTML = `<h1 class="panel-title">Latency</h1>
      <p class="muted" style="margin-top:0">Media start→end por agente / dossier (activity-log).</p>
      <div class="row-2">
        <div class="card-block"><h3 style="margin-top:0;font-size:1rem">Por agente</h3>
          <table class="data"><thead><tr><th>Agente</th><th>avg s</th><th>n</th></tr></thead><tbody>
          ${ag.map((r) => `<tr><td class="mono">${escapeHtml(r.agent || "")}</td><td>${escapeHtml(String(r.avg_sec ?? ""))}</td><td>${escapeHtml(String(r.samples ?? ""))}</td></tr>`).join("") || '<tr><td colspan="3" class="muted">—</td></tr>'}
          </tbody></table></div>
        <div class="card-block"><h3 style="margin-top:0;font-size:1rem">Por dossier</h3>
          <table class="data"><thead><tr><th>dossier</th><th>avg s</th><th>n</th></tr></thead><tbody>
          ${doss.map((r) => `<tr><td class="mono">${escapeHtml(r.dossier_id || "")}</td><td>${escapeHtml(String(r.avg_sec ?? ""))}</td><td>${escapeHtml(String(r.samples ?? ""))}</td></tr>`).join("") || '<tr><td colspan="3" class="muted">—</td></tr>'}
          </tbody></table></div>
      </div>`;
  } catch (e) {
    root.innerHTML = `<p class="err">${escapeHtml(e.message)}</p>`;
  }
}

async function renderCoverage(root, signal) {
  root.innerHTML = `<p class="muted">Cargando…</p>`;
  try {
    const [sk, hb] = await Promise.all([api("/v1/skills/coverage", { signal }), api("/v1/heartbeats/coverage", { signal })]);
    const sd = sk.data || {};
    const hd = hb.data || {};
    setViewExport({ skills: sd, heartbeats: hd });
    const rows = (sd.agents || []).map((r) => {
      const miss = !r.skill_md_count;
      const sh = r.shared_workspace ? ' <span class="muted">(compartido)</span>' : "";
      const wn = r.workspace_note ? ` <span class="muted" title="diagnóstico">${escapeHtml(r.workspace_note)}</span>` : "";
      return `<tr class="${miss ? "row-warn" : ""}"><td class="mono">${escapeHtml(r.agent_id || "")}</td><td>${escapeHtml(r.workspace || "")}${wn}</td><td>${escapeHtml(String(r.skill_md_count ?? 0))}${sh}</td></tr>`;
    });
    const byWs = (sd.by_workspace || []).map((g) => {
      const ids = (g.agent_ids || []).map((x) => `<span class="mono">${escapeHtml(x)}</span>`).join(", ");
      return `<tr><td class="mono">${escapeHtml(g.workspace || "")}</td><td>${ids}</td><td>${escapeHtml(String(g.skill_md_count ?? 0))}</td></tr>`;
    });
    const missHb = hd.missing_heartbeat || [];
    const hbrows = missHb.map((id) => `<tr><td class="mono">${escapeHtml(String(id))}</td><td>sin heartbeat</td></tr>`).join("");
    root.innerHTML = `<h1 class="panel-title">Coverage</h1>
      <p class="muted" style="margin-top:0"><span class="mono">/v1/skills/coverage</span> + <span class="mono">/v1/heartbeats/coverage</span></p>
      <div class="card-block"><h3 style="margin-top:0;font-size:1rem">SKILL.md por agente</h3>
        <table class="data"><thead><tr><th>Agente</th><th>workspace</th><th>SKILL.md</th></tr></thead><tbody>
        ${rows.join("") || '<tr><td colspan="3" class="muted">—</td></tr>'}
        </tbody></table></div>
      <div class="card-block" style="margin-top:1rem"><h3 style="margin-top:0;font-size:1rem">Skills por workspace (agrupado)</h3>
        <p class="muted" style="font-size:0.82rem">Misma carpeta <span class="mono">agents/&lt;grupo&gt;</span> compartida por varios <span class="mono">agent_id</span> (p. ej. marketing).</p>
        <table class="data"><thead><tr><th>Workspace</th><th>Agentes</th><th>SKILL.md</th></tr></thead><tbody>
        ${byWs.join("") || '<tr><td colspan="3" class="muted">—</td></tr>'}
        </tbody></table></div>
      <div class="card-block" style="margin-top:1rem"><h3 style="margin-top:0;font-size:1rem">Sin heartbeat</h3>
        <table class="data"><thead><tr><th>id</th><th>nota</th></tr></thead><tbody>
        ${hbrows || '<tr><td colspan="2" class="muted">Todos con heartbeat o lista vacía.</td></tr>'}
        </tbody></table></div>`;
  } catch (e) {
    root.innerHTML = `<p class="err">${escapeHtml(e.message)}</p>`;
  }
}

/** Vista Jerarquía: agrupa agent_id por carpeta workspace y lista skills (enlaces a lectura vía API). */
async function renderHierarchy(root, signal) {
  root.innerHTML = `<p class="muted">Cargando…</p>`;
  try {
    const [sk, oc] = await Promise.all([
      api("/v1/skills/coverage", { signal }),
      api("/v1/openclaw/agents", { signal }).catch(() => ({ data: {} })),
    ]);
    const sd = sk.data || {};
    const cfg = (oc.data && oc.data.config) || {};
    const lst = (cfg.agents && cfg.agents.list) || [];
    const hbById = {};
    for (const a of lst) {
      if (a && a.id) hbById[a.id] = a.heartbeat && Object.keys(a.heartbeat).length ? "sí" : "no";
    }
    const byWs = sd.by_workspace || [];
    setViewExport({ hierarchy: sd, openclaw_agents: lst });
    const blocks = byWs.map((g) => {
      const ws = escapeHtml(g.workspace || "");
      const agents = (g.agent_ids || [])
        .map((id) => {
          const hb = hbById[id] === "sí" ? " · heartbeat" : "";
          return `<li><span class="mono">${escapeHtml(id)}</span><span class="muted">${hb}</span></li>`;
        })
        .join("");
      const skills = (g.skill_slugs || [])
        .map((slug) => {
          const grp = String(g.workspace || "").replace(/^agents\//, "");
          const underAgents = `${grp}/skills/${slug}/SKILL.md`;
          return `<li><button type="button" class="btn btn--ghost jmc-skill-link" data-agents-path="${escapeHtml(underAgents)}" style="font-size:inherit;padding:0.1rem 0.4rem">${escapeHtml(slug)}</button></li>`;
        })
        .join("");
      return `<details class="card-block" style="margin-top:0.75rem" open>
        <summary><strong class="mono">${ws}</strong> — ${escapeHtml(String(g.skill_md_count ?? 0))} SKILL.md</summary>
        <div style="margin-top:0.5rem;display:grid;grid-template-columns:1fr 2fr;gap:1rem;align-items:start">
          <div><h4 class="muted" style="margin:0 0 0.25rem;font-size:0.85rem">Agentes</h4><ul style="margin:0;padding-left:1.2rem">${agents || '<li class="muted">—</li>'}</ul></div>
          <div><h4 class="muted" style="margin:0 0 0.25rem;font-size:0.85rem">Skills</h4><ul style="margin:0;padding-left:1.2rem;max-height:40vh;overflow:auto">${skills || '<li class="muted">—</li>'}</ul></div>
        </div></details>`;
    });
    root.innerHTML = `<h1 class="panel-title">Jerarquía</h1>
      <p class="muted" style="margin-top:0">Agrupación por carpeta <span class="mono">agents/&lt;grupo&gt;</span> (no hay árbol padre/hijo en <span class="mono">openclaw.json</span>).</p>
      ${blocks.join("") || '<p class="muted">Sin datos de cobertura.</p>'}`;
    root.querySelectorAll(".jmc-skill-link").forEach((btn) => {
      btn.onclick = () => {
        const p = btn.getAttribute("data-agents-path");
        if (!p) return;
        void (async () => {
          try {
            const u = `/v1/files/get?root=agents&path=${encodeURIComponent(p)}`;
            const j = await api(u, { signal });
            const c = (j.data && j.data.content) || "(sin contenido)";
            showModal(
              `<h3 style="margin-top:0"><span class="mono">${escapeHtml(p)}</span></h3><pre class="mono raw-block" style="max-height:70vh;overflow:auto;white-space:pre-wrap">${escapeHtml(c)}</pre>`
            );
          } catch (err) {
            showModal(`<p class="err">${escapeHtml(err.message)}</p>`);
          }
        })();
      };
    });
  } catch (e) {
    root.innerHTML = `<p class="err">${escapeHtml(e.message)}</p>`;
  }
}

async function renderCostsCompare(root, signal) {
  const m1 = root._ccM1 || currentMonthStr();
  const m2 = root._ccM2 || (() => {
    const [y, mo] = m1.split("-").map(Number);
    const d = new Date(y, mo - 2, 1);
    return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0");
  })();
  root.innerHTML = `<p class="muted">Cargando…</p>`;
  try {
    const [a, b] = await Promise.all([
      api("/v1/costs/summary?include_raw=0&month=" + encodeURIComponent(m1), { signal }),
      api("/v1/costs/summary?include_raw=0&month=" + encodeURIComponent(m2), { signal }),
    ]);
    const da = a.data || {};
    const db = b.data || {};
    setViewExport({ month_a: m1, month_b: m2, a: da, b: db });
    const ta = da.summary_line_total_tokens_est;
    const tb = db.summary_line_total_tokens_est;
    root.innerHTML = `<h1 class="panel-title">Costs compare</h1>
      <p class="muted" style="margin-top:0">Dos llamadas a <span class="mono">/v1/costs/summary?month=</span> (cliente).</p>
      <div class="toolbar"><label>Mes A <input type="month" id="cc-m1" value="${escapeHtml(m1)}" /></label>
        <label>Mes B <input type="month" id="cc-m2" value="${escapeHtml(m2)}" /></label>
        <button type="button" class="btn btn--primary" id="cc-reload">Recargar</button></div>
      <div class="grid-dashboard">
        <div class="stat-card"><div class="stat-label">${escapeHtml(m1)}</div><div class="stat-val">${escapeHtml(String(ta ?? "—"))}</div><div class="muted" style="font-size:0.8rem">tokens est.</div></div>
        <div class="stat-card"><div class="stat-label">${escapeHtml(m2)}</div><div class="stat-val">${escapeHtml(String(tb ?? "—"))}</div><div class="muted" style="font-size:0.8rem">tokens est.</div></div>
      </div>
      <p class="muted" style="font-size:0.82rem">Presupuesto blando (localStorage <span class="mono">jmc_budget</span>): <span id="cc-budget-hint"></span></p>`;
    root._ccM1 = m1;
    root._ccM2 = m2;
    let bud = 0;
    try {
      bud = Number(JSON.parse(localStorage.getItem("jmc_budget") || "{}").tokens_max || 0);
    } catch (_) {}
    const bh = root.querySelector("#cc-budget-hint");
    if (bh) bh.textContent = bud > 0 && ta != null && ta > bud ? `⚠ superado (${ta} > ${bud})` : bud ? `límite ${bud}` : "no configurado";
    const r1 = root.querySelector("#cc-m1");
    const r2 = root.querySelector("#cc-m2");
    const go = () => {
      root._ccM1 = r1 && r1.value ? r1.value : m1;
      root._ccM2 = r2 && r2.value ? r2.value : m2;
      renderCostsCompare(root, abortCtl.signal);
    };
    root.querySelector("#cc-reload").onclick = go;
  } catch (e) {
    root.innerHTML = `<p class="err">${escapeHtml(e.message)}</p>`;
  }
}

async function renderAbout(root, signal) {
  root.innerHTML = `<p class="muted">Cargando…</p>`;
  try {
    const j = await api("/v1/diagnostics", { signal });
    const d = j.data || {};
    const lj = await api("/v1/docs/lints", { signal }).catch(() => ({ data: {} }));
    const ld = lj.data || {};
    setViewExport({ diagnostics: d, docs_lints: ld });
    root.innerHTML = `<h1 class="panel-title">About / Diagnostics</h1>
      <p class="muted" style="margin-top:0"><span class="mono">/v1/diagnostics</span> · <span class="mono">/v1/docs/lints</span></p>
      <div class="card-block"><h3 style="margin-top:0;font-size:1rem">Runtime</h3>
        <pre class="mono raw-block" style="max-height:28vh;overflow:auto">${escapeHtml(JSON.stringify(d, null, 2))}</pre></div>
      <div class="card-block" style="margin-top:1rem"><h3 style="margin-top:0;font-size:1rem">Docs lints (resumen)</h3>
        <pre class="mono raw-block" style="max-height:28vh;overflow:auto">${escapeHtml(JSON.stringify(ld, null, 2))}</pre></div>
      <div class="toolbar" style="flex-wrap:wrap">
        <button type="button" class="btn btn--ghost" id="ab-copy-d">Copiar diagnostics JSON</button>
        <button type="button" class="btn btn--primary" id="ab-skill-tpl">Descargar SKILL.md plantilla</button>
      </div>
      <p class="muted" style="font-size:0.8rem">Webhook: <span class="mono">/v1/webhooks/status</span> · Trello: mapa en <span class="mono">localStorage jmc_trello_map</span> (JSON <code>{"AG-01":"https://..."}</code>).</p>`;
    root.querySelector("#ab-copy-d").onclick = () => void copyTextCatch(JSON.stringify(d, null, 2), "Copiado.");
    root.querySelector("#ab-skill-tpl").onclick = () => {
      const body = `---\nname: example-skill\ndescription: Describe la skill aquí.\n---\n\n# Example\n\n## Cuándo usar\n…\n`;
      downloadText("SKILL-template.md", body);
    };
  } catch (e) {
    root.innerHTML = `<p class="err">${escapeHtml(e.message)}</p>`;
  }
}

function downloadText(filename, text) {
  const blob = new Blob([text], { type: "text/markdown;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1500);
}

async function renderChat(root, signal) {
  if (root._chatPoll) {
    clearInterval(root._chatPoll);
    root._chatPoll = null;
  }
  root.innerHTML = `<p class="muted">Cargando…</p>`;
  let opts = {
    mirror_enabled: false,
    mirror_channels: ["telegram", "discord"],
    max_file_bytes: 26214400,
    max_files_per_message: 5,
  };
  try {
    const oj = await api("/v1/chat/options", { signal });
    Object.assign(opts, oj.data || {});
  } catch (_) {}
  const listJ = await api("/v1/chat/conversations", { signal });
  const items = (listJ.data && listJ.data.items) || [];
  if (!chatActiveConvId && items.length) chatActiveConvId = items[0].conv_id || "";
  if (chatActiveConvId && !items.some((x) => x.conv_id === chatActiveConvId)) {
    chatActiveConvId = items[0]?.conv_id || "";
  }
  persistFilters();

  let threadHtml = '<p class="muted chat-thread-empty">Cree una conversación o elija una de la lista.</p>';
  if (chatActiveConvId) {
    try {
      const cj = await api("/v1/chat/conversations/" + encodeURIComponent(chatActiveConvId), {
        signal,
        bypassCache: true,
      });
      const d = cj.data || {};
      const rows = d.messages || [];
      threadHtml =
        rows.length && window.JMC_CHAT
          ? `<div class="chat-thread" id="chat-thread-scroll">${window.JMC_CHAT.renderBubbles(chatActiveConvId, rows)}</div>`
          : '<p class="muted">Sin mensajes aún. Escriba abajo y pulse Enviar.</p>';
    } catch (e) {
      threadHtml = `<p class="err">${escapeHtml(e.message)}</p>`;
    }
  }

  const mb = Math.max(1, Math.round((opts.max_file_bytes || 26214400) / 1048576));
  const mf = opts.max_files_per_message || 5;
  root.innerHTML = `
    <h1 class="panel-title">Chat con Jarvis</h1>
    <p class="muted" style="margin-top:0">Buzón asíncrono bajo <span class="mono">state/jmc-inbox/</span>. Jarvis deja respuestas en <span class="mono">msg-*.reply.json</span> (ver docs).</p>
    <div class="chat-shell">
      <aside class="chat-sidebar">
        <button type="button" class="btn btn--primary" id="chat-new" style="width:100%;margin-bottom:0.5rem">Nueva conversación</button>
        <ul class="chat-conv-list">${items
          .map(
            (it) =>
              `<li><button type="button" class="chat-conv-btn ${it.conv_id === chatActiveConvId ? "active" : ""}" data-cid="${escapeHtml(
                it.conv_id
              )}">${escapeHtml(it.title || it.conv_id)}</button></li>`
          )
          .join("")}</ul>
      </aside>
      <div class="chat-main">
        <div class="chat-thread-wrap" id="chat-thread-wrap-el">${threadHtml}</div>
        <div class="chat-compose card-block">
          <label class="muted" for="chat-text">Mensaje</label>
          <textarea id="chat-text" class="input-token chat-textarea" rows="4" placeholder="Texto para Jarvis…"></textarea>
          <div class="chat-file-row" style="margin-top:0.35rem">
            <label class="btn btn--ghost btn-sm"><input type="file" id="chat-files" multiple style="display:none" />Adjuntar</label>
            <span class="muted" style="font-size:0.78rem;margin-left:0.5rem">Máx. ${mf} archivos · ${mb} MiB c/u</span>
          </div>
          <ul id="chat-file-pending" class="chat-pending-list"></ul>
          ${
            opts.mirror_enabled
              ? `<div style="margin:0.5rem 0"><label><input type="checkbox" id="chat-mirror-cb" /> Espejar a </label>
              <select id="chat-mirror-ch"><option value="">(no)</option>${(opts.mirror_channels || [])
                  .map((c) => `<option value="${escapeHtml(c)}">${escapeHtml(c)}</option>`)
                  .join("")}</select></div>`
              : `<p class="muted" style="font-size:0.78rem;margin:0.35rem 0">El espejo OpenClaw está <strong>desactivado</strong> en el servidor. Para activarlo, define <span class="mono">JMC_CHAT_MIRROR_ENABLED=1</span> (o <span class="mono">true</span>) y reinicia el adapter.</p>`
          }
          <div class="toolbar" style="margin-top:0.5rem">
            <button type="button" class="btn btn--primary" id="chat-send">Enviar</button>
            <button type="button" class="btn btn--ghost" id="chat-archive" ${chatActiveConvId ? "" : "disabled"}>Archivar</button>
          </div>
        </div>
      </div>
    </div>`;

  if (window.JMC_CHAT) window.JMC_CHAT.bindDownloads(root, getToken, getApiBase);

  const pending = [];
  const ful = root.querySelector("#chat-file-pending");
  function renderPending() {
    if (!ful) return;
    ful.innerHTML = pending
      .map(
        (f, i) =>
          `<li>${escapeHtml(f.name)} <span class="muted">(${f.size}b)</span> <button type="button" class="btn btn--ghost btn-sm" data-rm="${i}">✕</button></li>`
      )
      .join("");
    ful.querySelectorAll("[data-rm]").forEach((btn) => {
      btn.onclick = () => {
        pending.splice(parseInt(btn.getAttribute("data-rm"), 10), 1);
        renderPending();
      };
    });
  }

  const fu = root.querySelector("#chat-files");
  if (fu)
    fu.onchange = () => {
      for (const f of Array.from(fu.files || [])) pending.push(f);
      fu.value = "";
      renderPending();
    };

  root.querySelector("#chat-new").onclick = async () => {
    try {
      const j = await api("/v1/chat/conversations", { method: "POST", body: {} });
      const id = (j.data && j.data.conv_id) || "";
      if (id) {
        chatActiveConvId = id;
        persistFilters();
        await renderChat(root, abortCtl.signal);
      }
    } catch (e) {
      alert(errMessage(e));
    }
  };

  root.querySelectorAll(".chat-conv-btn").forEach((b) => {
    b.onclick = () => {
      chatActiveConvId = b.getAttribute("data-cid") || "";
      persistFilters();
      void renderChat(root, abortCtl.signal);
    };
  });

  const sendBtn = root.querySelector("#chat-send");
  if (sendBtn)
    sendBtn.onclick = async () => {
      const tid = chatActiveConvId;
      if (!tid) {
        alert("Cree o seleccione una conversación.");
        return;
      }
      const ta = root.querySelector("#chat-text");
      const tx = (ta && ta.value) || "";
      const fd = new FormData();
      fd.append("text", tx);
      const mcb = root.querySelector("#chat-mirror-cb");
      const mch = root.querySelector("#chat-mirror-ch");
      if (opts.mirror_enabled && mcb && mcb.checked && mch && mch.value) fd.append("mirror_channel", mch.value);
      for (const f of pending) fd.append("files", f, f.name);
      try {
        await api("/v1/chat/conversations/" + encodeURIComponent(tid) + "/messages", {
          method: "POST",
          body: fd,
          bypassCache: true,
        });
        pending.length = 0;
        renderPending();
        if (ta) ta.value = "";
        showToast("Mensaje enviado", "info");
        await renderChat(root, abortCtl.signal);
      } catch (e) {
        alert(errMessage(e));
      }
    };

  const arch = root.querySelector("#chat-archive");
  if (arch)
    arch.onclick = async () => {
      const tid = chatActiveConvId;
      if (!tid) return;
      if (!confirm("¿Archivar esta conversación?")) return;
      try {
        await api("/v1/chat/conversations/" + encodeURIComponent(tid) + "/archive", { method: "POST", body: {} });
        chatActiveConvId = "";
        persistFilters();
        await renderChat(root, abortCtl.signal);
      } catch (e) {
        alert(errMessage(e));
      }
    };

  setViewExport({ chat_options: opts, conversations: items, active_conv: chatActiveConvId });

  root._chatPoll = setInterval(async () => {
    if (currentView !== "chat" || !chatActiveConvId) return;
    const wrap = root.querySelector("#chat-thread-wrap-el");
    if (!wrap) return;
    try {
      const cj = await api("/v1/chat/conversations/" + encodeURIComponent(chatActiveConvId), {
        bypassCache: true,
        signal: abortCtl.signal,
      });
      const rows = (cj.data && cj.data.messages) || [];
      wrap.innerHTML =
        rows.length && window.JMC_CHAT
          ? `<div class="chat-thread" id="chat-thread-scroll">${window.JMC_CHAT.renderBubbles(chatActiveConvId, rows)}</div>`
          : '<p class="muted">Sin mensajes aún. Escriba abajo y pulse Enviar.</p>';
      if (window.JMC_CHAT) window.JMC_CHAT.bindDownloads(root, getToken, getApiBase);
    } catch (_) {}
  }, 8000);
}

const views = {
  overview: renderOverview,
  dossiers: renderDossiers,
  agents: renderAgents,
  hierarchy: renderHierarchy,
  tasks: renderTasks,
  costs: renderCosts,
  modes: renderModes,
  approvals: renderApprovals,
  escalations: renderEscalations,
  heartbeats: renderHeartbeats,
  gateway: renderGateway,
  system: renderSystem,
  cron: renderCron,
  memory: renderMemory,
  files: renderFiles,
  office: renderOffice,
  automations: renderAutomations,
  activity: renderActivity,
  chat: renderChat,
  gates: renderGates,
  health_deep: renderHealthDeep,
  errors: renderErrors,
  zombies: renderZombies,
  latency: renderLatency,
  coverage: renderCoverage,
  costs_compare: renderCostsCompare,
  about: renderAbout,
};

async function renderOverview(root, signal) {
  root.innerHTML = `<p class="muted">Cargando…</p>`;
  try {
    const settled = await Promise.allSettled([
      api("/v1/state/summary", { signal }),
      api("/v1/modes/current", { signal }),
      api("/v1/state/tasks", { signal }),
      api("/v1/state/handoffs", { signal }),
      api("/v1/escalations", { signal }),
      api("/v1/costs/summary?include_raw=0", { signal }),
      api("/v1/last30days", { signal }),
      api("/v1/state/activity?limit=15", { signal }),
      api("/v1/state/agents-stats", { signal }).catch(() => null),
    ]);
    const sumJ = settled[0].status === "fulfilled" ? settled[0].value : null;
    const modesJ = settled[1].status === "fulfilled" ? settled[1].value : null;
    const tasksJ = settled[2].status === "fulfilled" ? settled[2].value : null;
    const handJ = settled[3].status === "fulfilled" ? settled[3].value : null;
    const escJ = settled[4].status === "fulfilled" ? settled[4].value : null;
    const costJ = settled[5].status === "fulfilled" ? settled[5].value : null;
    const l30J = settled[6].status === "fulfilled" ? settled[6].value : null;

    const partial = [];
    if (settled[0].status === "rejected") partial.push("resumen: " + errMessage(settled[0].reason));
    if (settled[1].status === "rejected") partial.push("modo: " + errMessage(settled[1].reason));
    if (settled[2].status === "rejected") partial.push("tareas: " + errMessage(settled[2].reason));
    if (settled[3].status === "rejected") partial.push("handoffs: " + errMessage(settled[3].reason));
    if (settled[4].status === "rejected") partial.push("escalaciones: " + errMessage(settled[4].reason));
    if (settled[5].status === "rejected") partial.push("costes: " + errMessage(settled[5].reason));
    if (settled[6].status === "rejected") partial.push("30d: " + errMessage(settled[6].reason));
    if (settled[7].status === "rejected") partial.push("activity: " + errMessage(settled[7].reason));
    const summary = (sumJ && sumJ.data) || {};
    const m = (modesJ && modesJ.data) || {};
    const tasks = (tasksJ && tasksJ.data && tasksJ.data.tasks) || [];
    const hands = (handJ && handJ.data && handJ.data.handoffs) || [];
    const escn = escJ && escJ.data && escJ.data.items ? escJ.data.items.length : 0;
    const cd = (costJ && costJ.data) || {};
    const tok = cd.summary_line_total_tokens_est != null ? cd.summary_line_total_tokens_est : "—";
    const stalled = stalledTasks(tasks);
    const stalledCount = summary.stalled_tasks != null ? summary.stalled_tasks : stalled.length;
    const byDay = (l30J && l30J.data && l30J.data.by_day) || [];
    const sparkPts = byDay.map((d) => d.events || 0);
    const l30Ok = settled[6].status === "fulfilled";
    const actFeedJ = settled[7].status === "fulfilled" ? settled[7].value : null;
    const feedEvs = (actFeedJ && actFeedJ.data && actFeedJ.data.events) || [];
    const agStatsJ = settled[8].status === "fulfilled" ? settled[8].value : null;
    const agStats = (agStatsJ && agStatsJ.data) || {};
    const top24 = (agStats.top_agents_24h || []).slice(0, 8);
    const topErr = (agStats.top_errors_24h || []).slice(0, 6);
    const l30data = (l30J && l30J.data) || {};
    const totalEv30 = l30data.total_events;
    const numDays30 = byDay.length;
    const sparkCaption =
      l30Ok && totalEv30 != null && numDays30 > 0
        ? `<p class="muted" style="margin:0.35rem 0 0;font-size:0.8rem">${escapeHtml(String(totalEv30))} eventos en ${numDays30} día${numDays30 !== 1 ? "s" : ""}</p>`
        : "";

    const openT = summary.open_tasks != null ? summary.open_tasks : tasks.filter((t) => t.jmc_status === "open").length;

    let histPts = [];
    try {
      const h = JSON.parse(localStorage.getItem("jmc_overview_hist") || "[]");
      if (Array.isArray(h)) histPts = h.map((x) => Number(x.open) || 0).slice(-48);
    } catch (_) {}
    const histSpark =
      histPts.length > 1
        ? `<div class="card-block" style="margin-top:1rem"><h3 style="margin-top:0;font-size:1rem">Histórico local (tareas abiertas)</h3><p class="muted" style="margin:0 0 0.35rem;font-size:0.78rem">Muestras en <span class="mono">localStorage jmc_overview_hist</span> (cap 200).</p><div class="spark-wrap">${sparklineSVG(histPts)}</div></div>`
        : "";

    const warnBanner =
      partial.length > 0
        ? `<p class="muted" style="margin:0 0 1rem;padding:0.5rem 0.75rem;border:1px solid var(--border);border-radius:8px;background:rgba(251,191,36,0.08)">Algunos datos no cargaron: ${escapeHtml(partial.join(" · "))}</p>`
        : "";

    root.innerHTML = `
      <h1 class="panel-title">Overview</h1>
      <p class="toolbar" style="margin:0 0 0.75rem"><button type="button" class="btn btn--ghost btn-sm" id="ov-exec-sum">Resumen ejecutivo (export)</button></p>
      ${warnBanner}
      <div class="grid-dashboard">
        <div class="stat-card">${badgeMode(m.effective_mode)}<div class="stat-val">${escapeHtml(m.effective_mode || "?")}</div><div class="stat-label">Modo efectivo</div><p class="muted" style="margin:0.5rem 0 0;font-size:0.85rem">${escapeHtml(m.phrase || "")}</p></div>
        <button type="button" class="stat-card stat-card--click" data-kpi-nav="tasks-open" aria-label="Ir a Tasks, tareas abiertas">
          <div class="stat-label">Tareas abiertas</div><div class="stat-val">${openT}</div>
        </button>
        <button type="button" class="stat-card stat-card--click" data-kpi-nav="tasks-handoffs" aria-label="Ir a Tasks, sección handoffs">
          <div class="stat-label">Handoffs abiertos</div><div class="stat-val">${summary.open_handoffs != null ? summary.open_handoffs : hands.length}</div>
        </button>
        <button type="button" class="stat-card stat-card--click" data-kpi-nav="escalations" aria-label="Ir a Escalations">
          <div class="stat-label">Escalaciones</div><div class="stat-val">${escn}</div>
        </button>
        <button type="button" class="stat-card stat-card--click" data-kpi-nav="approvals" aria-label="Ir a Approvals">
          <div class="stat-label">AG pendientes</div><div class="stat-val">${summary.pending_approvals != null ? summary.pending_approvals : "—"}</div>
        </button>
        <button type="button" class="stat-card stat-card--click" data-kpi-nav="costs" aria-label="Ir a Costs">
          <div class="stat-label">Tokens mes (est.)</div><div class="stat-val">${escapeHtml(String(tok))}</div>
        </button>
      </div>
      <div class="row-2">
        <div class="card-block">
          <h3 style="margin-top:0;font-size:1rem">Actividad (30 días)</h3>
          <div class="spark-wrap">${l30Ok ? sparklineSVG(sparkPts) + sparkCaption : '<p class="muted">Sin datos de los últimos 30 días (endpoint no disponible — reinicie <span class="mono">jmc-adapter</span>).</p>'}</div>
          <p class="muted" style="margin:0.35rem 0 0;font-size:0.8rem">Eventos por día (últimos 30 días)</p>
        </div>
        <div class="card-block">
          <h3 style="margin-top:0;font-size:1rem">Tareas atrancadas (&gt;24h) · total ${escapeHtml(String(stalledCount))}</h3>
          ${stalled.length ? `<ul style="margin:0;padding-left:1.1rem;font-size:0.88rem">${stalled.slice(0, 8).map((t) => `<li><span class="mono">${escapeHtml(t.id || "")}</span> · ${escapeHtml(t.owner || "")}</li>`).join("")}</ul>` : '<p class="muted">Ninguna.</p>'}
        </div>
      </div>
      ${histSpark}
      <div class="row-2" style="margin-top:1rem">
        <div class="card-block">
          <h3 style="margin-top:0;font-size:1rem">Top agentes (24h)</h3>
          <table class="data"><thead><tr><th>Agente</th><th>Eventos</th></tr></thead><tbody>
          ${top24.length ? top24.map((r) => `<tr><td class="mono">${escapeHtml(r.agent || "")}</td><td>${escapeHtml(String(r.events ?? ""))}</td></tr>`).join("") : '<tr><td colspan="2" class="muted">—</td></tr>'}
          </tbody></table>
        </div>
        <div class="card-block">
          <h3 style="margin-top:0;font-size:1rem">Errores 24h (top)</h3>
          <table class="data"><thead><tr><th>Agente</th><th>Errores</th></tr></thead><tbody>
          ${topErr.length ? topErr.map((r) => `<tr><td class="mono">${escapeHtml(r.agent || "")}</td><td>${escapeHtml(String(r.errors ?? ""))}</td></tr>`).join("") : '<tr><td colspan="2" class="muted">—</td></tr>'}
          </tbody></table>
        </div>
      </div>
      <div class="card-block overview-feed-block" style="margin-top:1rem">
        <h3 style="margin-top:0;font-size:1rem">Actividad reciente</h3>
        <p class="muted" style="margin:0 0 0.5rem;font-size:0.82rem">Últimos eventos desde <span class="mono">activity-log</span> (misma fuente que la vista Activity).</p>
        ${
          feedEvs.length
            ? `<div class="overview-feed" role="feed" aria-label="Actividad reciente">${feedEvs.map((ev) => activityFeedLine(ev)).join("")}</div>`
            : '<p class="muted">Sin eventos recientes o feed no disponible.</p>'
        }
      </div>`;
    setViewExport({
      partial_errors: partial,
      summary,
      mode: m,
      tasks: tasks,
      handoffs: hands,
      escalations: escJ && escJ.data,
      costs: cd,
      last30days: l30data,
      activity_feed_sample: feedEvs,
    });
    try {
      const h = JSON.parse(localStorage.getItem("jmc_overview_hist") || "[]");
      const arr = Array.isArray(h) ? h : [];
      const tokN = cd.summary_line_total_tokens_est != null ? Number(cd.summary_line_total_tokens_est) : 0;
      arr.push({ t: Date.now(), open: Number(openT) || 0, tokens: Number.isFinite(tokN) ? tokN : 0 });
      while (arr.length > 200) arr.shift();
      localStorage.setItem("jmc_overview_hist", JSON.stringify(arr));
    } catch (_) {}
    const exBtn = root.querySelector("#ov-exec-sum");
    if (exBtn) {
      exBtn.onclick = () => {
        const md = `# Resumen ejecutivo JMC\n\n- Modo: **${m.effective_mode || "?"}** — ${m.phrase || ""}\n- Tareas abiertas: **${openT}**\n- Escalaciones (24h vista): **${escn}**\n- Tokens mes (est.): **${tok}**\n- Top agentes 24h: ${top24.map((r) => r.agent + "(" + r.events + ")").join(", ") || "—"}\n`;
        showModal(`<h2 style="margin-top:0">Resumen ejecutivo</h2><pre class="mono raw-block" style="white-space:pre-wrap">${escapeHtml(md)}</pre><p><button type="button" class="btn btn--primary" id="ov-exec-copy">Copiar Markdown</button></p>`);
        document.getElementById("ov-exec-copy").onclick = () => void copyTextCatch(md, "Copiado.");
      };
    }
    root.querySelectorAll("[data-kpi-nav]").forEach((btn) => {
      btn.onclick = () => {
        const nav = btn.getAttribute("data-kpi-nav");
        if (nav === "tasks-open") {
          taskFilter.status = "open";
          tasksViewMode = "table";
          persistFilters();
          activateTab("tasks");
          requestAnimationFrame(() => document.getElementById("main")?.querySelector(".tasks-table-wrap")?.scrollIntoView({ behavior: "smooth", block: "start" }));
        } else if (nav === "tasks-handoffs") {
          taskFilter.status = "all";
          tasksViewMode = "table";
          persistFilters();
          activateTab("tasks");
          requestAnimationFrame(() => {
            const hs = [...(document.getElementById("main")?.querySelectorAll("h2") || [])].find((h) =>
              (h.textContent || "").includes("Handoffs")
            );
            hs?.scrollIntoView({ behavior: "smooth", block: "start" });
          });
        } else if (nav === "escalations") activateTab("escalations");
        else if (nav === "approvals") {
          apFilters.ag = "";
          persistFilters();
          activateTab("approvals");
        } else if (nav === "costs") activateTab("costs");
      };
    });
    root.querySelectorAll(".feed-line--click").forEach((el) => {
      const go = () => {
        const ag = el.getAttribute("data-feed-agent") || "";
        actFilters.agent = ag;
        actCursor = null;
        persistFilters();
        activateTab("activity");
      };
      el.onclick = go;
      el.onkeydown = (e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          go();
        }
      };
    });
  } catch (e) {
    root.innerHTML = `<p class="err">${escapeHtml(e.message)}</p>`;
  }
}

let skillsLoaded = false;

function agentRowModel(a, fallbackModel) {
  return openclawModelString(a.model) || fallbackModel;
}

function agentToolsStr(a) {
  if (Array.isArray(a.tools)) return a.tools.join(", ");
  if (a.tools && typeof a.tools === "object") return JSON.stringify(a.tools);
  if (typeof a.tools === "string") return a.tools;
  return "";
}

function compareAgents(a, b, key, fallbackModel) {
  const va =
    key === "id"
      ? String(a.id || a.agentId || "")
      : key === "workspace"
        ? String(a.workspace || "")
        : agentRowModel(a, fallbackModel);
  const vb =
    key === "id"
      ? String(b.id || b.agentId || "")
      : key === "workspace"
        ? String(b.workspace || "")
        : agentRowModel(b, fallbackModel);
  return va.localeCompare(vb, undefined, { sensitivity: "base" });
}

async function renderAgents(root, signal) {
  root.innerHTML = `<p class="muted">Cargando…</p>`;
  try {
    const j = await api("/v1/openclaw/agents", { signal });
    const d = j.data || {};
    const cfg = d.config || {};
    let list = (cfg.agents && cfg.agents.list) || [];
    const defM = (cfg.agents && cfg.agents.defaults && cfg.agents.defaults.model) || "";
    const globM = (cfg.agent && cfg.agent.model) || "";
    const fallbackModel = openclawModelString(globM) || openclawModelString(defM);

    const q = agentsQuery.trim().toLowerCase();
    if (q) {
      list = list.filter((a) => {
        const blob = [a.id, a.agentId, a.workspace, agentRowModel(a, fallbackModel), a.mode, agentToolsStr(a)]
          .filter(Boolean)
          .join(" ")
          .toLowerCase();
        return blob.includes(q);
      });
    }

    list = list.slice().sort((a, b) => {
      const c = compareAgents(a, b, agentsSortKey, fallbackModel);
      return agentsSortDir === "asc" ? c : -c;
    });
    rebuildAgentUiMap(list);

    const hideModeCols = list.every((a) => !String(a.mode || "").trim() && !String(agentToolsStr(a)).trim());
    const colCount = hideModeCols ? 3 : 5;

    let skillsHtml = "";
    if (skillsLoaded) {
      const sk = await api("/v1/openclaw/skills", { signal });
      const ws = sk.data?.workspaces ?? {};
      skillsHtml =
        `<div class="card-block" style="margin-top:1rem"><h3 style="margin-top:0">Skills</h3>` +
        Object.keys(ws)
          .map((w) => {
            const items = ws[w] || [];
            return `<h4 class="muted" style="margin:0.75rem 0 0.35rem">${escapeHtml(w)}</h4><ul style="margin:0;font-size:0.85rem">${items.map((it) => `<li>${escapeHtml(it.name || "")} — ${escapeHtml((it.description || "").slice(0, 120))}</li>`).join("")}</ul>`;
          })
          .join("") +
        `</div>`;
    }

    const sortMark = (key) => (agentsSortKey === key ? (agentsSortDir === "asc" ? " ▲" : " ▼") : "");

    root.innerHTML = `
      <h1 class="panel-title">Agents</h1>
      <div class="toolbar" style="flex-wrap:wrap">
        <span class="muted">Densidad</span>
        <button type="button" class="chip ${uiDensity === "comfortable" ? "active" : ""}" data-ui-density="comfortable">Cómodo</button>
        <button type="button" class="chip ${uiDensity === "compact" ? "active" : ""}" data-ui-density="compact">Compacto</button>
      </div>
      <div class="toolbar" style="flex-wrap:wrap">
        <input type="search" id="agents-q" placeholder="Buscar id, workspace, modelo…" value="${escapeHtml(agentsQuery)}" style="min-width:14rem;flex:1" autocomplete="off" aria-label="Buscar agentes" />
        <button type="button" class="btn btn--primary" id="btn-skills">${skillsLoaded ? "Ocultar skills" : "Cargar skills"}</button>
      </div>
      <div style="overflow:auto">
      <table class="data agents-table" aria-label="Agentes OpenClaw">
        <thead><tr>
          <th scope="col"><button type="button" class="th-sort" data-sort="id">ID${sortMark("id")}</button></th>
          <th scope="col"><button type="button" class="th-sort" data-sort="workspace">Workspace${sortMark("workspace")}</button></th>
          <th scope="col"><button type="button" class="th-sort" data-sort="model">Modelo${sortMark("model")}</button></th>
          ${
            hideModeCols
              ? ""
              : `<th scope="col" title="Vacío hasta que el agente declare autonomy_mode en MEMORY.md (ver agents/jarvis/MEMORY.md)">Modo</th>
          <th scope="col">Tools</th>`
          }
        </tr></thead>
        <tbody>
        ${list
          .map((a) => {
            const id = a.id || a.agentId || "?";
            const ws = a.workspace || "";
            const model = agentRowModel(a, fallbackModel);
            const mode = a.mode || "";
            const tools = agentToolsStr(a);
            const toolsDisp = tools.length > 100 ? tools.slice(0, 100) + "…" : tools;
            const extra = hideModeCols
              ? ""
              : `<td>${escapeHtml(mode)}</td>
              <td style="font-size:0.78rem;max-width:14rem" title="${escapeHtml(tools)}">${escapeHtml(toolsDisp || "—")}</td>`;
            const av = agentAvatarHtml(id, a.ui || agentUiById[id]);
            return `<tr>
              <td class="mono" style="white-space:nowrap">${av}<strong>${escapeHtml(id)}</strong></td>
              <td style="font-size:0.85rem">${escapeHtml(ws)}</td>
              <td class="mono" style="font-size:0.8rem">${escapeHtml(model)}</td>
              ${extra}
            </tr>`;
          })
          .join("")}
        ${list.length === 0 ? `<tr><td colspan="${colCount}" class="muted">Ningún agente coincide con la búsqueda.</td></tr>` : ""}
        </tbody>
      </table>
      </div>
      ${skillsHtml}`;
    document.getElementById("btn-skills").onclick = () => {
      skillsLoaded = !skillsLoaded;
      renderAgents(root, abortCtl.signal);
    };
    let aqTimer;
    root.querySelector("#agents-q").oninput = (e) => {
      clearTimeout(aqTimer);
      const g = uiRenderGen;
      aqTimer = setTimeout(() => {
        if (g !== uiRenderGen) return;
        agentsQuery = e.target.value;
        persistFilters();
        renderAgents(root, abortCtl.signal);
      }, 280);
    };
    root.querySelectorAll(".th-sort").forEach((btn) => {
      btn.onclick = () => {
        const k = btn.getAttribute("data-sort");
        if (agentsSortKey === k) agentsSortDir = agentsSortDir === "asc" ? "desc" : "asc";
        else {
          agentsSortKey = k;
          agentsSortDir = "asc";
        }
        persistFilters();
        renderAgents(root, abortCtl.signal);
      };
    });
    root.querySelectorAll("[data-ui-density]").forEach((b) => {
      b.onclick = () => {
        uiDensity = b.getAttribute("data-ui-density");
        persistFilters();
        applyUiDensity();
        renderAgents(root, abortCtl.signal);
      };
    });
    setViewExport({ data: d, skillsLoaded, filtered_count: list.length });
  } catch (e) {
    root.innerHTML = `<p class="err">${escapeHtml(e.message)}</p>`;
  }
}

/** Texto de búsqueda precomputado por fila en Tasks (evita JSON.stringify en cada filtro). */
function taskRowSearchBlob(r) {
  return JSON.stringify({
    id: r.id,
    title: r.title,
    owner: r.owner,
    dossier_id: r.dossier_id,
    jmc_status: r.jmc_status,
    status: r.status,
    tags: r.tags,
    notes: r.notes,
    started_at: r.started_at,
    updated_at: r.updated_at,
  }).toLowerCase();
}

async function renderTasks(root, signal) {
  root.innerHTML = `<p class="muted">Cargando…</p>`;
  try {
    const settled = await Promise.allSettled([
      api("/v1/state/tasks", { signal }),
      api("/v1/state/handoffs", { signal }),
      api("/v1/state/pending_approvals", { signal }),
    ]);
    const ta = settled[0].status === "fulfilled" ? settled[0].value : { data: { tasks: [] } };
    const ha = settled[1].status === "fulfilled" ? settled[1].value : { data: { handoffs: [] } };
    const ap = settled[2].status === "fulfilled" ? settled[2].value : { data: { items: [] } };
    let actEvents = [];
    try {
      const actJ = await api("/v1/state/activity?limit=50", { signal });
      actEvents = actJ.data?.events ?? [];
    } catch (_) {
      actEvents = [];
    }
    const hands = ha.data?.handoffs ?? [];
    const allTasksRaw = ta.data?.tasks ?? [];
    const allTasks = allTasksRaw.map((r) => ({ ...r, _jmcSearchBlob: taskRowSearchBlob(r) }));
    const pendItems = ap.data?.items ?? [];
    const agMap = pendingAgByTask(pendItems);
    const agents = [...new Set(allTasks.map((r) => r.owner).filter(Boolean))].sort();
    const cAll = allTasks.length;
    const cOpen = allTasks.filter((r) => (r.jmc_status || "") === "open").length;
    const cWait = allTasks.filter((r) => (r.jmc_status || "") === "waiting_for_user").length;
    const cClosed = allTasks.filter((r) => (r.jmc_status || "") === "closed").length;

    const allTags = [
      ...new Set(allTasks.flatMap((r) => (Array.isArray(r.tags) ? r.tags.map(String) : []))),
    ].sort();
    const tagsAvailable = allTags.length > 0;
    const activeTags = Array.isArray(taskFilter.tags) ? taskFilter.tags.filter((t) => allTags.includes(t)) : [];
    if (activeTags.length !== (taskFilter.tags || []).length) {
      taskFilter.tags = activeTags;
      persistFilters();
    }

    let rows = allTasks.slice();
    if (taskFilter.status !== "all") {
      rows = rows.filter((r) => (r.jmc_status || "") === taskFilter.status);
    }
    if (taskFilter.agent) {
      rows = rows.filter((r) => (r.owner || "") === taskFilter.agent);
    }
    if (activeTags.length) {
      rows = rows.filter((r) => {
        const t = Array.isArray(r.tags) ? r.tags.map(String) : [];
        return activeTags.some((x) => t.includes(x));
      });
    }
    if (taskFilter.q) {
      const q = taskFilter.q.toLowerCase();
      rows = rows.filter((r) => (r._jmcSearchBlob || "").includes(q));
    }

    let rowsForBoard = allTasks.slice();
    if (taskFilter.agent) {
      rowsForBoard = rowsForBoard.filter((r) => (r.owner || "") === taskFilter.agent);
    }
    if (activeTags.length) {
      rowsForBoard = rowsForBoard.filter((r) => {
        const t = Array.isArray(r.tags) ? r.tags.map(String) : [];
        return activeTags.some((x) => t.includes(x));
      });
    }
    if (taskFilter.q) {
      const q = taskFilter.q.toLowerCase();
      rowsForBoard = rowsForBoard.filter((r) => (r._jmcSearchBlob || "").includes(q));
    }

    const chips = [
      ["all", `Todos (${cAll})`],
      ["open", `open (${cOpen})`],
      ["waiting_for_user", `wait (${cWait})`],
      ["closed", `closed (${cClosed})`],
    ];
    const tagCountsMap = taskTagCountsMap(allTasks);
    const tagBar = tagsAvailable
      ? `<div class="tag-toolbar"><span class="muted" style="font-size:0.78rem">Tags (conteo total):</span>${allTags
          .map((t) => {
            const cnt = tagCountsMap[t] || 0;
            const hue = tagHue(t);
            return `<button type="button" class="tag-chip tag-chip--hue ${activeTags.includes(t) ? "active" : ""}" style="--tag-hue:${hue}deg" data-tag="${escapeHtml(t)}">${escapeHtml(t)}<span class="tag-count" aria-label="tareas con este tag">${cnt}</span></button>`;
          })
          .join("")}${activeTags.length ? `<button type="button" class="btn btn--ghost" id="flt-tags-clear" style="font-size:0.74rem;padding:0.2rem 0.5rem">Limpiar tags</button>` : ""}</div>`
      : "";
    const tagHeader = tagsAvailable ? "<th>Tags</th>" : "";
    const showTable = tasksViewMode === "table";
    const nowMs = Date.now();
    const actIdx = buildActivityIndexesFromEvents(actEvents, nowMs);
    const boardCols = groupTasksByBoardCol(rowsForBoard, agMap, actIdx, nowMs);
    const taskIdSet = new Set(allTasks.map((t) => String(t.id || "").trim()).filter(Boolean));
    for (const it of pendItems) {
      const tid = String(it.task_id || "").trim();
      if (!tid || taskIdSet.has(tid)) continue;
      boardCols.review.push({
        id: tid,
        jmc_status: "waiting_for_user",
        title: `AG pendiente · ${it.schema || "handoff"}`,
        owner: String(it.from || it.to || ""),
        dossier_id: it.dossier_id,
        _jmc_orphan_placeholder: true,
        _jmc_orphan_ag: it.ag,
      });
    }
    const mcColOrder = [
      ["inbox", "Inbox"],
      ["in_progress", "In progress"],
      ["review", "Review"],
      ["blocked", "Blocked"],
      ["done", "Done"],
    ];
    const boardFilterMap = { inbox: "open", in_progress: "open", review: "waiting_for_user", blocked: "open", done: "closed" };
    const railMap = agentsRailCountsFromTasks(allTasks);
    const ownersSorted = [...railMap.keys()].sort((a, b) => {
      if (a === "—") return 1;
      if (b === "—") return -1;
      return a.localeCompare(b);
    });
    const railHtml = `
      <aside class="agents-rail ${tasksBoardRailCollapsed ? "agents-rail--collapsed" : ""}" aria-label="Agentes y conteos">
        <div class="agents-rail-head">
          <strong>Agentes</strong>
          <button type="button" class="btn btn--ghost btn-rail-toggle" id="btn-rail-toggle" title="Ocultar panel">${tasksBoardRailCollapsed ? "»" : "«"}</button>
        </div>
        <div class="agents-rail-body">
          <button type="button" class="rail-agent rail-agent--all ${!taskFilter.agent ? "active" : ""}" data-rail-agent="">Todos</button>
          ${ownersSorted
            .map((owner) => {
              const c = railMap.get(owner) || { open: 0, wait: 0, closed: 0 };
              const active = taskFilter.agent === owner;
              return `<button type="button" class="rail-agent ${active ? "active" : ""}" data-rail-agent="${escapeHtml(owner)}">
                <span class="rail-agent-id mono">${escapeHtml(owner)}</span>
                <span class="rail-agent-counts muted" title="open / wait / closed">o${c.open} · w${c.wait} · c${c.closed}</span>
              </button>`;
            })
            .join("")}
        </div>
      </aside>`;
    const chipToolbarHtml =
      tasksViewMode === "board"
        ? chips
            .filter(([v]) => v === "all")
            .map(
              ([v, lab]) =>
                `<button type="button" class="chip active" data-chip="${v}" title="En Tablero las columnas muestran todos los estados; este chip no aplica filtro de estado al tablero.">${escapeHtml(lab)}</button>`
            )
            .join("") +
          `<span class="muted" style="font-size:0.78rem;margin-left:0.35rem" title="El filtro open/wait/closed solo afecta a la vista Tabla.">Estado por columnas</span>`
        : chips.map(([v, lab]) => `<button type="button" class="chip ${taskFilter.status === v ? "active" : ""}" data-chip="${v}">${escapeHtml(lab)}</button>`).join("");

    const kanbanMcHtml = `
      <div class="tasks-board-mc-wrap${tasksBoardRailCollapsed ? " tasks-board-mc-wrap--rail-collapsed" : ""}" ${showTable ? "hidden" : ""}>
        ${railHtml}
        <div class="tasks-kanban-mc" role="region" aria-label="Tablero estilo Mission Control (solo lectura)">
        ${mcColOrder
          .map(([colId, lab]) => {
            const colRows = boardCols[colId] || [];
            const coarse = boardFilterMap[colId] || "all";
            return `
        <div class="kanban-col kanban-col--mc" data-board-col="${colId}">
          <button type="button" class="kanban-col-head-btn" data-board-filter="${escapeHtml(colId)}" data-coarse-status="${escapeHtml(coarse)}" title="Filtrar por estado JMC aproximado">
            <span class="kanban-col-title">${escapeHtml(lab)}</span>
            <span class="kanban-col-count muted">(${colRows.length})</span>
          </button>
          <div class="kanban-col-body">
            ${colRows.length ? colRows.map((r) => window.JMC_KANBAN.kanbanCardHtml(r, agMap, tagsAvailable, `kanban-card--col-${colId}`, { escapeHtml, badgeTask, fmtRel, tagHue, taskDurationMs, fmtDurMs })).join("") : window.JMC_KANBAN.emptyColumnHtml(taskBoardHasExtraFilters(), escapeHtml, lab)}
          </div>
        </div>`;
          })
          .join("")}
        </div>
      </div>`;
    root.innerHTML = `
      <h1 class="panel-title">Tasks &amp; Handoffs</h1>
      <div class="toolbar tasks-view-toolbar">
        <span class="muted">Vista</span>
        <button type="button" class="chip ${tasksViewMode === "table" ? "active" : ""}" data-task-view="table">Tabla</button>
        <button type="button" class="chip ${tasksViewMode === "board" ? "active" : ""}" data-task-view="board">Tablero</button>
        <span class="muted">Densidad</span>
        <button type="button" class="chip ${uiDensity === "comfortable" ? "active" : ""}" data-ui-density="comfortable">Cómodo</button>
        <button type="button" class="chip ${uiDensity === "compact" ? "active" : ""}" data-ui-density="compact">Compacto</button>
        ${
          tasksViewMode === "board" && tasksBoardRailCollapsed
            ? `<button type="button" class="chip chip--rail-show" id="btn-rail-show" title="Mostrar panel de agentes">Mostrar agentes</button>`
            : ""
        }
      </div>
      <div class="toolbar">
        ${chipToolbarHtml}
        <select id="flt-agent" aria-label="Filtrar por agente propietario"><option value="">Todos los agentes</option>${agents.map((a) => `<option value="${escapeHtml(a)}" ${taskFilter.agent === a ? "selected" : ""}>${escapeHtml(a)}</option>`).join("")}</select>
        <input type="search" id="flt-q" placeholder="Buscar…" value="${escapeHtml(taskFilter.q)}" aria-label="Buscar en tareas" />
        <button type="button" class="btn btn--ghost" id="flt-clear">Limpiar filtros</button>
      </div>
      ${tagBar}
      ${kanbanMcHtml}
      <div class="tasks-table-wrap" ${showTable ? "" : "hidden"}>
      <table class="data tasks-data-table"><thead><tr><th>ID</th><th>Estado</th><th>AG</th><th>Owner</th><th>Dossier</th><th>Ref</th><th>Inicio</th><th>Duración</th>${tagHeader}</tr></thead><tbody>
      ${
        rows.length
          ? rows
              .map(
                (r) => {
                  const tid = r.id || "";
                  const ag = agMap[tid];
                  const agHtml = ag ? `<span class="badge-ag">${escapeHtml(ag)}</span>` : "—";
                  const dur = fmtDurMs(taskDurationMs(r));
                  const tagsCell = tagsAvailable
                    ? `<td>${(Array.isArray(r.tags) ? r.tags.map(String) : [])
                        .map((t) => `<span class="tag-chip tag-chip--hue" style="--tag-hue:${tagHue(t)}deg">${escapeHtml(t)}</span>`)
                        .join("") || "—"}</td>`
                    : "";
                  return `<tr class="click-row" data-task="${escapeHtml(tid)}"><td class="mono">${escapeHtml((tid || "").slice(0, 36))}</td><td>${badgeTask(r)}</td><td>${agHtml}</td><td>${escapeHtml(r.owner || "")}</td><td class="mono">${escapeHtml(r.dossier_id || "")}</td><td>${escapeHtml(r.ref || "")}</td><td>${fmtRel(r.started_at)}</td><td class="muted">${escapeHtml(dur)}</td>${tagsCell}</tr>`;
                }
              )
              .join("")
          : `<tr><td colspan="${8 + (tagsAvailable ? 1 : 0)}" class="tasks-table-empty muted">
            Sin tareas con los filtros actuales (p. ej. <span class="mono">open(0)</span>).
            <button type="button" class="btn btn--ghost btn-sm" id="flt-clear-table">Limpiar filtros</button>
          </td></tr>`
      }
      </tbody></table>
      </div>
      <h2 style="margin-top:1.5rem;font-size:1rem">Handoffs (${hands.length})</h2>
      ${window.JMC_TABLES.renderDataTable(
        [
          { key: "file", label: "Archivo" },
          { key: "fromto", label: "From→To" },
          { key: "schema", label: "Schema" },
          { key: "task_id", label: "task_id" },
        ],
        hands.map((h) => ({
          file: h._file || "",
          fromto: `${h.from || ""} → ${h.to || ""}`,
          schema: h.schema || h.kind || "",
          task_id: h.task_id || "",
        }))
      )}`;

    root.querySelectorAll("[data-task-view]").forEach((b) => {
      b.onclick = () => {
        tasksViewMode = b.getAttribute("data-task-view");
        persistFilters();
        renderTasks(root, abortCtl.signal);
      };
    });
    root.querySelectorAll("[data-ui-density]").forEach((b) => {
      b.onclick = () => {
        uiDensity = b.getAttribute("data-ui-density");
        persistFilters();
        applyUiDensity();
        renderTasks(root, abortCtl.signal);
      };
    });
    root.querySelectorAll("[data-chip]").forEach((b) => {
      b.onclick = () => {
        taskFilter.status = b.getAttribute("data-chip");
        persistFilters();
        renderTasks(root, abortCtl.signal);
      };
    });
    root.querySelector("#flt-agent").onchange = (e) => {
      taskFilter.agent = e.target.value;
      persistFilters();
      renderTasks(root, abortCtl.signal);
    };
    let qtimer;
    root.querySelector("#flt-q").oninput = (e) => {
      clearTimeout(qtimer);
      const g = uiRenderGen;
      qtimer = setTimeout(() => {
        if (g !== uiRenderGen) return;
        taskFilter.q = e.target.value;
        persistFilters();
        renderTasks(root, abortCtl.signal);
      }, 300);
    };
    const clearTaskFilters = () => {
      taskFilter = { status: "open", agent: "", q: "", tags: [] };
      persistFilters();
      renderTasks(root, abortCtl.signal);
    };
    const clr = root.querySelector("#flt-clear");
    if (clr) clr.onclick = clearTaskFilters;
    const clrt = root.querySelector("#flt-clear-table");
    if (clrt) clrt.onclick = clearTaskFilters;
    root.querySelectorAll("[data-tag]").forEach((btn) => {
      btn.onclick = () => {
        const tag = btn.getAttribute("data-tag");
        const cur = new Set(taskFilter.tags || []);
        if (cur.has(tag)) cur.delete(tag);
        else cur.add(tag);
        taskFilter.tags = [...cur];
        persistFilters();
        renderTasks(root, abortCtl.signal);
      };
    });
    const tagsClr = root.querySelector("#flt-tags-clear");
    if (tagsClr)
      tagsClr.onclick = () => {
        taskFilter.tags = [];
        persistFilters();
        renderTasks(root, abortCtl.signal);
      };

    tasksCacheForPalette = allTasks;
    const rt = root.querySelector("#btn-rail-toggle");
    if (rt)
      rt.onclick = () => {
        tasksBoardRailCollapsed = !tasksBoardRailCollapsed;
        persistFilters();
        renderTasks(root, abortCtl.signal);
      };
    const rs = root.querySelector("#btn-rail-show");
    if (rs)
      rs.onclick = () => {
        tasksBoardRailCollapsed = false;
        persistFilters();
        renderTasks(root, abortCtl.signal);
      };
    root.querySelectorAll(".btn-flt-clear-board").forEach((b) => {
      b.onclick = () => {
        taskFilter.agent = "";
        taskFilter.q = "";
        taskFilter.tags = [];
        persistFilters();
        renderTasks(root, abortCtl.signal);
      };
    });
    root.querySelectorAll("[data-rail-agent]").forEach((btn) => {
      btn.onclick = () => {
        if (btn.classList.contains("rail-agent--all")) {
          taskFilter.agent = "";
        } else {
          const v = btn.getAttribute("data-rail-agent") || "";
          if (taskFilter.agent === v) taskFilter.agent = "";
          else taskFilter.agent = v;
        }
        persistFilters();
        renderTasks(root, abortCtl.signal);
      };
    });
    root.querySelectorAll("[data-board-filter]").forEach((btn) => {
      btn.onclick = () => {
        const coarse = btn.getAttribute("data-coarse-status") || "open";
        taskFilter.status = coarse;
        persistFilters();
        renderTasks(root, abortCtl.signal);
      };
    });

    root.querySelectorAll(".click-row").forEach((tr) => {
      tr.onclick = () => {
        const tid = tr.getAttribute("data-task");
        if (!tid) return;
        openTaskModal(tid);
      };
    });
    const boardExportCounts = {};
    mcColOrder.forEach(([cid]) => {
      boardExportCounts[cid] = (boardCols[cid] || []).length;
    });
    setViewExport({
      taskFilter,
      tasksViewMode,
      uiDensity,
      tasksBoardRailCollapsed,
      tasks: allTasks,
      filtered_tasks: rows,
      handoffs: hands,
      pending_approvals: pendItems,
      board: {
        columns: boardExportCounts,
        activity_tail_used: actEvents.length,
        derive: "mission_control_readonly_v1.7",
      },
    });
  } catch (e) {
    root.innerHTML = `<p class="err">${escapeHtml(e.message)}</p>`;
  }
}

function currentMonthStr() {
  const d = new Date();
  return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0");
}

async function renderCosts(root, signal) {
  const month = root._costMonth || currentMonthStr();
  const raw = !!root._costRaw;
  root.innerHTML = `<p class="muted">Cargando…</p>`;
  try {
    const j = await api("/v1/costs/summary?include_raw=" + (raw ? "1" : "0") + (month ? "&month=" + encodeURIComponent(month) : ""), { signal });
    const d = j.data || {};
    const norm = d.agents_normalized || {};
    const total = d.summary_line_total_tokens_est;
    const agents = Object.keys(d.agents || {});
    const apiMonth = d.month || "";
    const monthMismatch = apiMonth && apiMonth !== month;
    const normBroken =
      agents.length > 0 &&
      agents.every((k) => {
        const n = norm[k];
        if (!n || typeof n !== "object") return true;
        return (
          n.sessions_active == null &&
          n.tokens_total == null &&
          n.tokens_in == null &&
          !(n.top_models && n.top_models.length) &&
          n.messages_user == null &&
          n.messages_assistant == null
        );
      });
    const normHint = normBroken
      ? `<p class="muted" style="margin:0 0 1rem;padding:0.5rem;border-radius:8px;border:1px solid var(--border);background:rgba(251,191,36,0.08)">Datos no normalizados (<code>agents_normalized</code> vacío) — verifique versión del adapter y reinicie <span class="mono">jmc-adapter</span>.</p>`
      : "";
    const monthLine =
      `<p class="muted" style="margin:0 0 0.75rem;font-size:0.82rem">Mes del reporte: <span class="mono">${escapeHtml(apiMonth || "—")}</span>${monthMismatch ? ` · solicitado en UI: <span class="mono">${escapeHtml(month)}</span>` : ""}</p>`;
    let maxTok = 1;
    for (const name of agents) {
      const n = norm[name] || {};
      const tin = Number(n.tokens_in) || 0;
      const tout = Number(n.tokens_out) || 0;
      maxTok = Math.max(maxTok, tin + tout);
    }
    const modelTotals = new Map();
    for (const name of agents) {
      const n = norm[name] || {};
      for (const x of n.top_models || []) {
        const mk = String(x.model || "?");
        modelTotals.set(mk, (modelTotals.get(mk) || 0) + (Number(x.count) || 0));
      }
    }
    const topModelsGlobal = [...modelTotals.entries()].sort((a, b) => b[1] - a[1]).slice(0, 5);
    const topModelsHtml = topModelsGlobal.length
      ? `<div class="cost-model-chips">${topModelsGlobal.map(([m, c]) => `<span class="model-chip mono">${escapeHtml(m)} <span class="muted">(${c})</span></span>`).join("")}</div>`
      : `<p class="muted">Sin desglose por modelo.</p>`;
    root.innerHTML = `
      <h1 class="panel-title">Costs</h1>
      ${normHint}
      ${monthLine}
      <div class="toolbar">
        <label>Mes <input type="month" id="cost-month" value="${escapeHtml(String(month))}" aria-label="Mes del reporte de costes" /></label>
        <label><input type="checkbox" id="cost-raw" ${raw ? "checked" : ""} aria-label="Mostrar raw del reporte"/> Mostrar raw</label>
      </div>
      <div class="stat-card" style="margin-bottom:1rem"><div class="stat-label">Total tokens est. (mes)</div><div class="stat-val">${total != null ? escapeHtml(redactIfDemo(String(total))) : "—"}</div>${getDemoMode() ? `<p class="muted" style="font-size:0.78rem">Modo demo: <span class="mono">localStorage jmc_demo=1</span> oculta cifras.</p>` : ""}${d.error ? `<p class="err">${escapeHtml(d.error)}</p>` : ""}</div>
      ${agents
        .map((name) => {
          const n = norm[name] || {};
          const tin = Number(n.tokens_in) || 0;
          const tout = Number(n.tokens_out) || 0;
          const wIn = Math.min(100, Math.round((tin / maxTok) * 100));
          const wOut = Math.min(100, Math.round((tout / maxTok) * 100));
          const chips = (n.top_models || [])
            .map((x) => `<span class="model-chip mono">${escapeHtml(String(x.model || "?"))} <span class="muted">(${escapeHtml(String(x.count ?? ""))})</span></span>`)
            .join("");
          return `<div class="cost-agent-card card-block"><h4>${escapeHtml(name)}</h4>
            <div class="cost-bar-wrap" title="IN vs OUT (escala = máx IN+OUT entre agentes este mes)">
              <div class="cost-bar-legend muted"><span>IN</span><span>OUT</span></div>
              <div class="cost-bar-track">
                <div class="cost-bar-in" style="width:${wIn}%"></div>
                <div class="cost-bar-out" style="width:${wOut}%"></div>
              </div>
            </div>
            <div class="cost-metrics">
            <div><span>Sesiones</span> ${escapeHtml(String(n.sessions_active != null ? Number(n.sessions_active) : "—"))}</div>
            <div><span>Msgs U/A</span> ${escapeHtml(String(n.messages_user != null ? Number(n.messages_user) : "—"))} / ${escapeHtml(String(n.messages_assistant != null ? Number(n.messages_assistant) : "—"))}</div>
            <div><span>Tok IN/OUT/T</span> ${escapeHtml(String(n.tokens_in != null ? Number(n.tokens_in) : "—"))} / ${escapeHtml(String(n.tokens_out != null ? Number(n.tokens_out) : "—"))} / ${escapeHtml(String(n.tokens_total != null ? Number(n.tokens_total) : "—"))}</div>
            <div style="grid-column:1/-1"><span>Modelos</span> ${chips || '<span class="muted">—</span>'}</div>
          </div></div>`;
        })
        .join("")}
      <div class="card-block cost-aggregate-card"><h3 style="margin-top:0;font-size:1rem">Agregado mensual (top modelos)</h3>${topModelsHtml}</div>
      ${raw && d.raw_tail ? `<pre class="raw-block mono">${escapeHtml(d.raw_tail)}</pre>` : ""}`;
    root._costMonth = month;
    root._costRaw = raw;
    setViewExport({ month, raw, data: d });
    const mi = root.querySelector("#cost-month");
    if (mi)
      mi.onchange = () => {
        root._costMonth = mi.value;
        renderCosts(root, abortCtl.signal);
      };
    const cr = root.querySelector("#cost-raw");
    if (cr)
      cr.onchange = () => {
        root._costRaw = cr.checked;
        renderCosts(root, abortCtl.signal);
      };
  } catch (e) {
    root.innerHTML = `<p class="err">${escapeHtml(e.message)}</p>`;
  }
}

async function renderModes(root, signal) {
  root.innerHTML = `<p class="muted">Cargando…</p>`;
  try {
    const settled = await Promise.allSettled([api("/v1/modes/current", { signal }), api("/v1/modes/matrix", { signal })]);
    const cur = settled[0].status === "fulfilled" ? settled[0].value : null;
    const mx = settled[1].status === "fulfilled" ? settled[1].value : null;
    const curErr = settled[0].status === "rejected" ? errMessage(settled[0].reason) : null;
    const mxErr = settled[1].status === "rejected" ? errMessage(settled[1].reason) : null;

    const m = (cur && cur.data) || {};
    if (!curErr) {
      lastModeWriteEnabled = !!m.mode_write_enabled;
      updateSidebarFoot();
    }
    const matrix = (mx && mx.data && mx.data.matrix) || [];
    const mm = m.memory_modes || {};
    const mmList = Object.keys(mm).length
      ? `<ul style="font-size:0.88rem">${Object.entries(mm).map(([k, v]) => `<li><span class="mono">${escapeHtml(k)}</span> → ${badgeMode(v)}</li>`).join("")}</ul>`
      : `<p class="muted modes-memory-hint" style="margin:0">Ningún <code>agents/*/MEMORY.md</code> declara <code>autonomy_mode</code> aún. <button type="button" class="btn-link-quiet" id="modes-autonomia-doc">Ver doc</button></p>`;

    const phrases = m.mode_phrases || {};
    const letters = ["A", "B", "C", "D"];
    const eff = String(m.effective_mode || "D").toUpperCase().slice(0, 1);
    const modeOpts = letters
      .map((letter) => {
        const ph = phrases[letter] || "";
        const short = ph.length > 80 ? ph.slice(0, 80) + "…" : ph;
        const sel = eff === letter ? " selected" : "";
        return `<option value="${letter}"${sel}>${letter} — ${escapeHtml(short)}</option>`;
      })
      .join("");
    const modeWriteOn = !!m.mode_write_enabled;
    const applyBtnClass = modeWriteOn ? "btn btn--primary" : "btn btn--ghost";
    const applyBtnLabel = modeWriteOn ? "Aplicar" : "Mostrar comandos";
    const applyBtnTitle = modeWriteOn
      ? "Escribir JARVIS_AUTONOMY_MODE en ~/.openclaw/.env y en el proceso del adapter"
      : "No cambia el modo en pantalla: abre los comandos para copiar y aplicar en tu shell o .env";
    const applyBlock = curErr
      ? ""
      : `<div class="modes-apply-wrap" style="margin-top:0.75rem">
        <div class="modes-apply-toolbar toolbar" style="flex-wrap:wrap;align-items:center;gap:0.5rem">
        <label for="mode-select" class="muted">Cambiar modo</label>
        <select id="mode-select" aria-label="Seleccionar modo A B C o D" style="min-width:12rem;max-width:min(42vw,28rem)">${modeOpts}</select>
        <button type="button" class="${applyBtnClass}" id="mode-apply" title="${escapeHtml(applyBtnTitle)}">${escapeHtml(applyBtnLabel)}</button>
        ${
          modeWriteOn
            ? `<span class="badge badge--closed" title="POST /v1/modes/current escribe ~/.openclaw/.env (o JMC_OPENCLAW_ENV_PATH)">Write ON</span>`
            : `<span class="badge badge--wait" title="La API indicó solo lectura: use comandos manuales">Read-only</span>`
        }
      </div>
      ${
        modeWriteOn
          ? ""
          : `<p class="muted modes-readonly-hint" style="margin:0.45rem 0 0;font-size:0.78rem;max-width:42rem">Si la API devolviera solo lectura, este botón <strong>no</strong> escribiría en disco: solo rellenaría el panel de comandos para copiarlos.</p>`
      }
      </div>
      <div id="modes-manual-panel" class="card-block modes-manual-panel" hidden style="margin-top:0.75rem">
        <h3 style="margin:0 0 0.5rem;font-size:0.95rem">Comandos para aplicar manualmente</h3>
        <p class="muted" style="margin:0 0 0.35rem;font-size:0.78rem">Export (shell actual):</p>
        <pre class="mono raw-block modes-manual-pre" id="modes-manual-export"></pre>
        <p class="muted" style="margin:0.5rem 0 0.35rem;font-size:0.78rem">Línea en archivo <span class="mono">.env</span>:</p>
        <pre class="mono raw-block modes-manual-pre" id="modes-manual-envline"></pre>
        <button type="button" class="btn btn--ghost" id="modes-copy-manual">Copiar ambos</button>
      </div>`;

    const modeBlock = curErr
      ? `<p class="err">Modo actual no disponible: ${escapeHtml(curErr)}</p>`
      : `<div class="card-block" style="margin-bottom:1rem">
        ${badgeMode(m.effective_mode)}
        <p style="margin:0.5rem 0 0">${escapeHtml(m.phrase || "")}</p>
        <p class="muted" style="margin:0.75rem 0 0">${
          modeWriteOn
            ? "Pulse <strong>Aplicar</strong> para escribir <span class=\"mono\">JARVIS_AUTONOMY_MODE</span> en tu <span class=\"mono\">.env</span> y en el proceso del adapter (requiere Bearer en Conexión)."
            : "La API indicó solo lectura: use los comandos manuales de abajo."
        } ${escapeHtml(m.doc_ref || "")}</p>
        ${applyBlock}
        <h3 style="margin:1rem 0 0.35rem">MEMORY por agente</h3>
        ${mmList}
      </div>`;

    const matrixWarn = mxErr
      ? `<p class="muted" style="margin:0 0 0.75rem;padding:0.5rem;border-radius:8px;border:1px solid var(--border);background:rgba(251,191,36,0.08)">Matriz no disponible: ${escapeHtml(mxErr)} — actualice y reinicie <span class="mono">jmc-adapter</span> si persiste.</p>`
      : "";

    const apiUnreliable = !getToken() || lastHealthOk === false;
    const apiHealthBanner = apiUnreliable
      ? `<p class="muted" role="status" style="margin:0 0 0.75rem;padding:0.5rem;border-radius:8px;border:1px solid var(--border);background:rgba(251,191,36,0.08)">Sin conexión fiable con el adapter (<span class="mono">/v1/health</span> falla o falta token). Abra <strong>Conexión</strong>, guarde el Bearer y use el mismo host/puerto donde corre <span class="mono">jmc-adapter</span>. Los datos aquí pueden estar en caché o desactualizados; espere <strong>API OK</strong> en la cabecera antes de confiar en cambios en vivo.</p>`
      : "";

    const remoteBase = getApiBase();
    const pageOrig =
      typeof window !== "undefined" && window.location && window.location.origin ? window.location.origin : "";
    const originMismatch = Boolean(remoteBase && pageOrig && remoteBase !== pageOrig);
    const originBanner = originMismatch
      ? `<p class="muted" role="status" style="margin:0 0 0.75rem;padding:0.5rem;border-radius:8px;border:1px solid var(--border);background:rgba(251,191,36,0.08)">La URL base del API en <strong>Conexión</strong> (<span class="mono">${escapeHtml(remoteBase)}</span>) no coincide con el origen de esta página (<span class="mono">${escapeHtml(pageOrig)}</span>). Revise el puerto (p. ej. <span class="mono">8765</span> frente a un typo) o deje la URL vacía para usar la misma pestaña.</p>`
      : "";

    const mq = modesQuery.trim().toLowerCase();
    const matrixFiltered = mq
      ? matrix.filter((row) => {
          const blob = [row.gate_id, row.label, row.D, row.C, row.B, row.A].join(" ").toLowerCase();
          return blob.includes(mq);
        })
      : matrix;

    root.innerHTML = `
      <h1 class="panel-title">Modes</h1>
      ${apiHealthBanner}
      ${originBanner}
      ${modeBlock}
      <h2 style="font-size:1rem">Matriz AG × Modo</h2>
      ${matrixWarn}
      <div class="toolbar" style="margin-bottom:0.75rem">
        <input type="search" id="modes-q" placeholder="Buscar gate o agente…" value="${escapeHtml(modesQuery)}" aria-label="Buscar en matriz de modos" style="min-width:16rem;flex:1" autocomplete="off" />
      </div>
      <div style="overflow:auto">
        <table class="data">
          <thead><tr><th>Gate</th><th>D</th><th>C</th><th>B</th><th>A</th></tr></thead>
          <tbody>
          ${matrixFiltered.length
            ? matrixFiltered
                .map(
                  (row) =>
                    `<tr><td><strong>${escapeHtml(row.gate_id)}</strong> ${escapeHtml(row.label)}</td><td class="mat-cell ${matrixCellClass(row.D)}">${escapeHtml(row.D)}</td><td class="mat-cell ${matrixCellClass(row.C)}">${escapeHtml(row.C)}</td><td class="mat-cell ${matrixCellClass(row.B)}">${escapeHtml(row.B)}</td><td class="mat-cell ${matrixCellClass(row.A)}">${escapeHtml(row.A)}</td></tr>`
                )
                .join("")
            : `<tr><td colspan="5" class="muted">${mxErr ? "—" : mq ? "Ninguna fila coincide con la búsqueda." : "Sin filas en docs/AUTONOMIA_MODOS.md"}</td></tr>`}
          </tbody>
        </table>
      </div>`;
    let mqTimer;
    const mqi = root.querySelector("#modes-q");
    if (mqi)
      mqi.oninput = () => {
        clearTimeout(mqTimer);
        const g = uiRenderGen;
        mqTimer = setTimeout(() => {
          if (g !== uiRenderGen) return;
          modesQuery = mqi.value;
          persistFilters();
          renderModes(root, abortCtl.signal);
        }, 280);
      };

    const docBtn = root.querySelector("#modes-autonomia-doc");
    if (docBtn) {
      docBtn.onclick = async () => {
        try {
          const j = await api("/v1/modes/doc_fragment", { bypassCache: true });
          const sn = (j.data && j.data.snippet) || "";
          showModal(
            `<h2 style="margin-top:0">${escapeHtml((j.data && j.data.path) || "AUTONOMIA_MODOS.md")}</h2><pre class="mono raw-block" style="max-height:60vh;overflow:auto">${escapeHtml(sn)}</pre>`
          );
        } catch (err) {
          showToast(errMessage(err), "warn");
        }
      };
    }

    const fillManual = (letter, hint) => {
      const panel = root.querySelector("#modes-manual-panel");
      const ex = root.querySelector("#modes-manual-export");
      const ln = root.querySelector("#modes-manual-envline");
      if (!panel || !ex || !ln) return;
      const h = hint || {};
      ex.textContent = h.export || "export JARVIS_AUTONOMY_MODE=" + letter;
      ln.textContent = h.env_line || "JARVIS_AUTONOMY_MODE=" + letter;
      panel.hidden = false;
    };

    const applyBtn = root.querySelector("#mode-apply");
    const sel = root.querySelector("#mode-select");
    if (applyBtn && sel && !curErr) {
      applyBtn.onclick = async () => {
        const letter = String(sel.value || "D").toUpperCase().slice(0, 1);
        if (!modeWriteOn) {
          fillManual(letter, null);
          showToast(
            "Solo lectura: el modo mostrado arriba en JMC no cambia hasta ejecutar los comandos en tu shell o en el .env.",
            "info"
          );
          return;
        }
        const prev = String(m.effective_mode || "D").toUpperCase().slice(0, 1);
        const rank = { D: 0, C: 1, B: 2, A: 3 };
        const rPrev = rank[prev] != null ? rank[prev] : 0;
        const rNew = rank[letter] != null ? rank[letter] : 0;
        const regression = rNew < rPrev;
        const doPost = async () => {
          try {
            apiCache.clear();
            await api("/v1/modes/current", { method: "POST", body: { mode: letter }, bypassCache: true });
            try {
              const hist = JSON.parse(localStorage.getItem("jmc_mode_hist") || "[]");
              const a = Array.isArray(hist) ? hist : [];
              a.push({ t: Date.now(), from: prev, to: letter });
              while (a.length > 80) a.shift();
              localStorage.setItem("jmc_mode_hist", JSON.stringify(a));
            } catch (_) {}
            showToast("Modo aplicado: " + letter, "ok");
            renderModes(root, abortCtl.signal);
          } catch (e) {
            let hint = null;
            try {
              const parsed = JSON.parse(e.message);
              if (parsed && parsed.error && parsed.error.hint) hint = parsed.error.hint;
            } catch (_) {}
            if (hint) {
              fillManual(letter, hint);
              showToast("Escritura deshabilitada en el servidor.", "warn");
            } else showToast(errMessage(e), "warn");
          }
        };
        showModal(`<h2 style="margin-top:0">Confirmar cambio de modo</h2>
          <p>Pasar de <strong>${escapeHtml(prev)}</strong> → <strong>${escapeHtml(letter)}</strong>. Esto escribe <span class="mono">JARVIS_AUTONOMY_MODE</span> en el <span class="mono">.env</span> configurado.</p>
          ${regression ? `<p class="err" style="font-size:0.9rem">Posible regresión de autonomía (modo numéricamente más bajo). Revise <span class="mono">docs/AUTONOMIA_MODOS.md</span> y <span class="mono">APPROVAL_GATES.md</span>.</p>` : ""}
          <p class="muted" style="font-size:0.82rem">Checklist CEO (cliente): pendientes AG, escalaciones, heartbeats silent — revise vistas <strong>Approvals</strong>, <strong>Escalations</strong>, <strong>Gateway</strong>.</p>
          <p style="margin-top:1rem"><button type="button" class="btn btn--primary" id="mode-wiz-go">Aplicar</button> <button type="button" class="btn btn--ghost" id="mode-wiz-cancel">Cancelar</button></p>`);
        document.getElementById("mode-wiz-cancel").onclick = () => hideModal();
        document.getElementById("mode-wiz-go").onclick = () => {
          hideModal();
          void doPost();
        };
      };
    }

    const copyM = root.querySelector("#modes-copy-manual");
    if (copyM) {
      copyM.onclick = () => {
        const ex = root.querySelector("#modes-manual-export");
        const ln = root.querySelector("#modes-manual-envline");
        const t = (ex && ex.textContent ? ex.textContent : "") + "\n" + (ln && ln.textContent ? ln.textContent : "");
        void copyTextCatch(t, "Copiado al portapapeles.");
      };
    }

    setViewExport({ current: m, matrix, matrix_filtered_count: matrixFiltered.length, errors: { curErr, mxErr } });
  } catch (e) {
    root.innerHTML = `<p class="err">${escapeHtml(e.message)}</p>`;
  }
}

async function renderEscalations(root, signal) {
  root.innerHTML = `<p class="muted">Cargando…</p>`;
  try {
    const j = await api("/v1/escalations", { signal });
    const items = j.data?.items ?? [];
    if (!items.length) {
      root.innerHTML = `<h1 class="panel-title">Escalations</h1><p class="muted">Sin tareas en espera del usuario. Cuando un gate requiera decisión, aparecerán aquí. Ref: ${escapeHtml(j.data?.doc_ref ?? "")}</p>`;
      setViewExport({ items: [], doc_ref: j.data?.doc_ref });
      return;
    }
    root.innerHTML =
      `<h1 class="panel-title">Escalations</h1>` +
      items
        .map(
          (it, i) =>
            `<div class="esc-card">
            <div style="display:flex;justify-content:space-between;align-items:start;gap:0.5rem">
              <div><strong>${escapeHtml(it.id || "")}</strong> ${badgeTask(it)} · ${escapeHtml(it.owner || "")}</div>
              <button type="button" class="btn btn--primary btn-copy-esc" data-idx="${i}">Copiar payload</button>
            </div>
            <p class="muted" style="margin:0.35rem 0">${escapeHtml(it.title || "")}</p>
            <p style="margin:0;font-size:0.85rem"><span class="muted">dossier</span> <span class="mono">${escapeHtml(it.dossier_id || "")}</span> · ref ${escapeHtml(it.ref || "")}</p>
          </div>`
        )
        .join("");
    root.querySelectorAll(".btn-copy-esc").forEach((btn) => {
      btn.onclick = () => {
        const i = Number(btn.getAttribute("data-idx"));
        void copyTextCatch(JSON.stringify(items[i], null, 2), null);
      };
    });
    setViewExport({ items });
  } catch (e) {
    root.innerHTML = `<p class="err">${escapeHtml(e.message)}</p>`;
  }
}

async function renderActivity(root, signal) {
  const actLimit = Math.min(500, Math.max(10, parseInt(String(actFilters.limit), 10) || 80));
  const q =
    "/v1/state/activity?limit=" +
    actLimit +
    (actFilters.agent ? "&agent=" + encodeURIComponent(actFilters.agent) : "") +
    (actFilters.kind ? "&kind=" + encodeURIComponent(actFilters.kind) : "") +
    (actFilters.since ? "&since=" + encodeURIComponent(actFilters.since) : "") +
    (actCursor ? "&cursor=" + encodeURIComponent(actCursor) : "");

  root.innerHTML = `<p class="muted">Cargando…</p>`;
  try {
    let tagStats = {};
    try {
      const ts = await api("/v1/state/tag-stats", { signal });
      tagStats = (ts.data && ts.data.tag_counts) || {};
    } catch (_) {
      tagStats = {};
    }
    const j = await api(q, { signal });
    const data = j.data || {};
    let evs = data.events || [];
    const tagF = String(actFilters.tag || "").trim();
    if (tagF) evs = evs.filter((ev) => eventMatchesTagFilter(ev, tagF));
    const groupBy = actFilters.group || "flat";
    const groupOpts = [
      ["flat", "Plana"],
      ["by_task", "Por task"],
      ["by_dossier", "Por dossier"],
    ];
    const groupChips = groupOpts
      .map(
        ([v, lab]) =>
          `<button type="button" class="chip ${groupBy === v ? "active" : ""}" data-group="${v}">${escapeHtml(lab)}</button>`
      )
      .join("");

    let timelineHtml = "";
    if (groupBy === "flat") {
      timelineHtml = `<div class="timeline">${evs.map((ev) => activityEventHtml(ev)).join("")}</div>`;
    } else {
      const key = groupBy === "by_task" ? "task_id" : "dossier_id";
      const buckets = new Map();
      evs.forEach((ev) => {
        const k = String(ev[key] || "—");
        if (!buckets.has(k)) buckets.set(k, []);
        buckets.get(k).push(ev);
      });
      const sorted = [...buckets.entries()].sort((a, b) => (a[0] === "—" ? 1 : b[0] === "—" ? -1 : a[0].localeCompare(b[0])));
      timelineHtml = sorted
        .map(
          ([k, items]) =>
            `<details class="tl-group" open><summary class="tl-group-head"><span class="mono">${escapeHtml(k)}</span> <span class="muted">· ${items.length} evento${items.length !== 1 ? "s" : ""}</span></summary><div class="timeline timeline--grouped">${items.map((ev) => activityEventHtml(ev)).join("")}</div></details>`
        )
        .join("");
    }

    const kindOpts = [
      ["", "Todos tipos"],
      ["start", "start"],
      ["event", "event"],
      ["end", "end"],
      ["handoff", "handoff"],
    ];
    const kindChips = kindOpts
      .map(
        ([v, lab]) =>
          `<button type="button" class="chip ${(actFilters.kind || "") === v ? "active" : ""}" data-act-kind="${escapeHtml(v)}">${escapeHtml(lab)}</button>`
      )
      .join("");
    const tagKeys = Object.keys(tagStats).sort();
    const tagChips =
      tagKeys.length > 0
        ? `<div class="toolbar" style="flex-wrap:wrap"><span class="muted" style="font-size:0.82rem">Tag (cliente):</span>
        <button type="button" class="chip ${!actFilters.tag ? "active" : ""}" data-act-tag="">Todos</button>
        ${tagKeys
          .map(
            (tg) =>
              `<button type="button" class="chip ${actFilters.tag === tg ? "active" : ""}" data-act-tag="${escapeHtml(tg)}">${escapeHtml(tg)} <span class="muted">(${tagStats[tg]})</span></button>`
          )
          .join("")}</div>`
        : "";

    root.innerHTML = `
      <h1 class="panel-title">Activity</h1>
      <div class="toolbar" style="flex-wrap:wrap">
        <span class="muted">Densidad</span>
        <button type="button" class="chip ${uiDensity === "comfortable" ? "active" : ""}" data-ui-density="comfortable">Cómodo</button>
        <button type="button" class="chip ${uiDensity === "compact" ? "active" : ""}" data-ui-density="compact">Compacto</button>
      </div>
      <div class="toolbar">
        <input type="text" id="act-agent" placeholder="agent" value="${escapeHtml(actFilters.agent)}" aria-label="Filtrar por agente" />
        <input type="text" id="act-kind" placeholder="type (texto)" value="${escapeHtml(actFilters.kind)}" aria-label="Tipo de evento (texto libre)" title="Sincronizado con chips de tipo debajo" />
        <input type="text" id="act-tag" placeholder="tag (substring)" value="${escapeHtml(actFilters.tag)}" aria-label="Filtrar por tag en payload" />
        <input type="text" id="act-since" placeholder="since ISO" value="${escapeHtml(actFilters.since)}" aria-label="Desde fecha ISO" />
        <input type="number" id="act-limit" min="10" max="500" value="${escapeHtml(String(actLimit))}" style="width:5rem" aria-label="Límite de eventos"/>
        <button type="button" class="btn btn--primary" id="act-go">Aplicar</button>
      </div>
      <div class="toolbar" style="flex-wrap:wrap"><span class="muted" style="font-size:0.82rem">Tipo:</span> ${kindChips}</div>
      ${tagChips}
      <div class="toolbar"><span class="muted" style="font-size:0.82rem">Agrupar:</span> ${groupChips}</div>
      ${timelineHtml || '<p class="muted">Sin eventos para los filtros actuales.</p>'}
      ${data.next_cursor ? `<p><button type="button" class="btn" id="act-more">Más (cursor)</button></p>` : ""}`;

    root.querySelector("#act-go").onclick = () => {
      actFilters.agent = root.querySelector("#act-agent").value.trim();
      actFilters.kind = root.querySelector("#act-kind").value.trim();
      actFilters.tag = root.querySelector("#act-tag").value.trim();
      actFilters.since = root.querySelector("#act-since").value.trim();
      actFilters.limit = Math.min(500, Math.max(10, parseInt(root.querySelector("#act-limit").value, 10) || 80));
      actCursor = null;
      persistFilters();
      renderActivity(root, abortCtl.signal);
    };
    root.querySelectorAll("[data-act-kind]").forEach((b) => {
      b.onclick = () => {
        actFilters.kind = b.getAttribute("data-act-kind") || "";
        const ik = root.querySelector("#act-kind");
        if (ik) ik.value = actFilters.kind;
        actCursor = null;
        persistFilters();
        renderActivity(root, abortCtl.signal);
      };
    });
    root.querySelectorAll("[data-act-tag]").forEach((b) => {
      b.onclick = () => {
        actFilters.tag = b.getAttribute("data-act-tag") || "";
        const it = root.querySelector("#act-tag");
        if (it) it.value = actFilters.tag;
        actCursor = null;
        persistFilters();
        renderActivity(root, abortCtl.signal);
      };
    });
    root.querySelectorAll("[data-ui-density]").forEach((b) => {
      b.onclick = () => {
        uiDensity = b.getAttribute("data-ui-density");
        persistFilters();
        applyUiDensity();
        renderActivity(root, abortCtl.signal);
      };
    });
    root.querySelectorAll("[data-group]").forEach((b) => {
      b.onclick = () => {
        actFilters.group = b.getAttribute("data-group");
        persistFilters();
        renderActivity(root, abortCtl.signal);
      };
    });
    const more = root.querySelector("#act-more");
    if (more) {
      more.onclick = () => {
        actCursor = data.next_cursor;
        renderActivity(root, abortCtl.signal);
      };
    }
    setViewExport({
      filters: { ...actFilters },
      cursor: actCursor,
      events: data.events,
      next_cursor: data.next_cursor,
    });
  } catch (e) {
    root.innerHTML = `<p class="err">${escapeHtml(e.message)}</p>`;
  }
}

async function renderGateway(root, signal) {
  root.innerHTML = `<p class="muted">Cargando…</p>`;
  try {
    const wh = gatewayWindowHours;
    const [j, actJ] = await Promise.all([
      api("/v1/openclaw/gateway?window_hours=" + encodeURIComponent(String(wh)), { signal }),
      api("/v1/state/activity?limit=300", { signal }).catch(() => ({ data: { events: [] } })),
    ]);
    const d = j.data || {};
    const actTail = (actJ.data && actJ.data.events) || [];
    const lastByAgent = new Map();
    for (const ev of actTail) {
      const ag = String(ev.agent || "").trim();
      if (!ag) continue;
      const ts = Date.parse(ev.ts || "");
      if (Number.isNaN(ts)) continue;
      const prev = lastByAgent.get(ag);
      if (prev == null || ts > prev) lastByAgent.set(ag, ts);
    }
    const agents = d.agents || [];
    const totals = d.totals || {};
    const byKind = totals.by_kind || [];
    const silentN = agents.filter((a) => a.silent).length;
    const aliveN = agents.length - silentN;
    const presetBtns = [
      [1, "1h"],
      [6, "6h"],
      [24, "24h"],
      [168, "7d"],
    ];
    const winChips = presetBtns
      .map(
        ([h, lab]) =>
          `<button type="button" class="chip ${gatewayWindowHours === h ? "active" : ""}" data-gw-win="${h}">${escapeHtml(lab)}</button>`
      )
      .join("");
    root.innerHTML = `
      <h1 class="panel-title">Gateway runtime (ventana ${escapeHtml(String(d.window_hours || wh))}h)</h1>
      <div class="toolbar" style="flex-wrap:wrap">
        <span class="muted">Densidad</span>
        <button type="button" class="chip ${uiDensity === "comfortable" ? "active" : ""}" data-ui-density="comfortable">Cómodo</button>
        <button type="button" class="chip ${uiDensity === "compact" ? "active" : ""}" data-ui-density="compact">Compacto</button>
      </div>
      <div class="toolbar" style="flex-wrap:wrap;align-items:center;gap:0.35rem">
        <span class="muted" style="font-size:0.82rem">Ventana:</span>
        ${winChips}
      </div>
      <p class="muted" style="margin-top:0">Derivado de <span class="mono">state/activity-log.jsonl</span> + <span class="mono">openclaw.json</span>.</p>
      <div class="card-block gw-info-box" style="margin-bottom:1rem;font-size:0.88rem">
        <strong>Qué significa SILENT</strong>
        <p class="muted" style="margin:0.35rem 0 0">Los contadores de esta vista usan solo eventos dentro de la ventana seleccionada (<span class="mono">${escapeHtml(String(d.window_hours || wh))}h</span>).
        <strong>SILENT</strong> = ningún evento de ese agente en esa ventana. Si cambias a <strong>7d</strong> o revisas que los agentes escriban en <span class="mono">activity-log</span>, pueden aparecer como vivos.
        Si un agente sigue SILENT pero ves una fecha en <em>Último evento (log)</em>, ese evento cayó fuera de la ventana Gateway.</p>
      </div>
      <div class="grid-dashboard">
        <div class="stat-card"><div class="stat-label">Eventos (ventana)</div><div class="stat-val">${escapeHtml(String(totals.events_24h || 0))}</div><div class="stat-sub muted">${escapeHtml(String(d.window_hours || wh))}h</div></div>
        <div class="stat-card"><div class="stat-label">Agentes vivos</div><div class="stat-val">${aliveN}</div></div>
        <div class="stat-card"><div class="stat-label">Agentes silenciosos</div><div class="stat-val">${silentN}</div></div>
      </div>
      <h2 style="margin-top:1rem;font-size:1rem">Agentes</h2>
      ${
        agents.length
          ? `<table class="data"><thead><tr><th>ID</th><th>Estado</th><th>Last seen (ventana)</th><th>Último evento (log)</th><th>Eventos (ventana)</th><th>Heartbeats (ventana)</th><th>Configurado</th></tr></thead><tbody>
      ${agents
        .map((a) => {
          const stCls = a.silent ? "badge--wait" : "badge--closed";
          const stLab = a.silent ? "silent" : "alive";
          const tsG = lastByAgent.get(a.id);
          const logCell =
            tsG != null
              ? `<span class="muted gw-log-ts" title="Máx. ts en últimos 300 eventos del activity-log (puede estar fuera de la ventana)">${escapeHtml(fmtRel(new Date(tsG).toISOString()) || "—")}</span>`
              : "—";
          return `<tr><td class="mono">${escapeHtml(a.id)}</td><td><span class="badge ${stCls}">${stLab}</span></td><td class="muted" title="${escapeHtml(a.last_seen || "")}">${a.last_seen ? fmtRel(a.last_seen) : "—"}</td><td>${logCell}</td><td>${escapeHtml(String(a.events_24h))}</td><td>${escapeHtml(String(a.heartbeats_24h))}</td><td>${a.configured ? "sí" : "—"}</td></tr>`;
        })
        .join("")}
      </tbody></table>`
          : '<p class="muted">Sin actividad ni agentes configurados.</p>'
      }
      <h2 style="margin-top:1rem;font-size:1rem">Top tipos de evento</h2>
      ${
        byKind.length
          ? `<table class="data"><thead><tr><th>Tipo</th><th>Conteo</th></tr></thead><tbody>${byKind.map((k) => `<tr><td>${badgeEv(k.kind)}</td><td>${escapeHtml(String(k.count))}</td></tr>`).join("")}</tbody></table>`
          : '<p class="muted">Sin eventos.</p>'
      }`;
    root.querySelectorAll("[data-ui-density]").forEach((b) => {
      b.onclick = () => {
        uiDensity = b.getAttribute("data-ui-density");
        persistFilters();
        applyUiDensity();
        renderGateway(root, abortCtl.signal);
      };
    });
    root.querySelectorAll("[data-gw-win]").forEach((b) => {
      b.onclick = () => {
        const n = Number(b.getAttribute("data-gw-win"));
        if (!Number.isFinite(n)) return;
        gatewayWindowHours = Math.max(1, Math.min(168, Math.round(n)));
        persistFilters();
        renderGateway(root, abortCtl.signal);
      };
    });
    setViewExport({ gateway_window_hours_requested: wh, ...d });
  } catch (e) {
    root.innerHTML = `<p class="err">${escapeHtml(e.message)}</p>`;
  }
}

async function renderGates(root, signal) {
  root.innerHTML = `<p class="muted">Cargando…</p>`;
  try {
    const j = await api("/v1/gates", { signal });
    const gates = j.data?.gates ?? [];
    root.innerHTML = `
      <h1 class="panel-title">Gates AG-01..AG-13</h1>
      <div class="toolbar" style="flex-wrap:wrap;gap:0.35rem">
        <input type="search" id="gate-q" placeholder="Filtrar…" aria-label="Filtrar tabla de gates" style="min-width:12rem;flex:1" />
        <button type="button" class="btn btn--ghost btn-sm" id="gate-glosario">Glosario AG (aprox.)</button>
      </div>
      <table class="data" id="gate-table"><thead><tr><th>ID</th><th>Acción</th><th>Agentes</th><th>Nivel</th><th>Cómo solicitar</th><th></th></tr></thead><tbody>
      ${gates
        .map(
          (g) =>
            `<tr data-text="${escapeHtml((g.id + " " + g.action + " " + g.agents + " " + g.level).toLowerCase())}"><td class="mono">${escapeHtml(g.id)}</td><td>${escapeHtml(g.action)}</td><td>${escapeHtml(g.agents)}</td><td>${escapeHtml(g.level)}</td><td style="font-size:0.82rem">${escapeHtml(g.how_to_request)}</td><td><button type="button" class="btn btn--ghost btn-sm gate-to-ap" data-gate-id="${escapeHtml(g.id)}">Ver approvals</button></td></tr>`
        )
        .join("")}
      </tbody></table>`;
    const gl = root.querySelector("#gate-glosario");
    if (gl) {
      gl.onclick = () => {
        const body = gates
          .map((g) => `- **${g.id}**: ${g.action} — agentes: ${g.agents}; nivel ${g.level}; ${g.how_to_request}`)
          .join("\n");
        showModal(
          `<h2 style="margin-top:0">Glosario AG (cliente)</h2>
          <p class="muted" style="font-size:0.82rem">Resumen desde <span class="mono">/v1/gates</span>. Ver fuente en <span class="mono">docs/APPROVAL_GATES.md</span>.</p>
          <pre class="mono raw-block" style="max-height:55vh;overflow:auto;white-space:pre-wrap">${escapeHtml(body)}</pre>
          <p><button type="button" class="btn btn--primary" id="gate-glo-copy">Copiar Markdown</button></p>`
        );
        const c = document.getElementById("gate-glo-copy");
        if (c) c.onclick = () => void copyTextCatch("# Glosario AG\n\n" + body, "Copiado.");
      };
    }
    const inp = root.querySelector("#gate-q");
    inp.oninput = () => {
      const q = inp.value.toLowerCase();
      root.querySelectorAll("#gate-table tbody tr").forEach((tr) => {
        const t = tr.getAttribute("data-text") || "";
        tr.style.display = !q || t.includes(q) ? "" : "none";
      });
    };
    root.querySelectorAll(".gate-to-ap").forEach((btn) => {
      btn.onclick = () => {
        apFilters.ag = btn.getAttribute("data-gate-id") || "";
        persistFilters();
        activateTab("approvals");
      };
    });
    setViewExport({ gates });
  } catch (e) {
    root.innerHTML = `<p class="err">${escapeHtml(e.message)}</p>`;
  }
}

function getDemoMode() {
  try {
    return localStorage.getItem("jmc_demo") === "1";
  } catch (_) {
    return false;
  }
}

function redactIfDemo(s) {
  if (!getDemoMode()) return s;
  const t = String(s);
  if (/^\d+$/.test(t)) return "•••";
  if (t.length > 12) return t.slice(0, 4) + "…";
  return t;
}

function navRoleFilter(viewId) {
  let r = "";
  try {
    r = String(localStorage.getItem("jmc_role") || "").trim().toLowerCase();
  } catch (_) {}
  if (r === "soporte" && (viewId === "costs" || viewId === "costs_compare" || viewId === "modes")) return false;
  if (r === "ceo") return true;
  return true;
}

function buildSidebar() {
  const nav = document.getElementById("sidebar-nav");
  const rows = NAV.filter(([id]) => navRoleFilter(id));
  nav.innerHTML = rows.map(
    ([id, label, ico]) =>
      `<button type="button" class="nav-btn" data-view="${id}" data-role="all"><span class="nav-ico" aria-hidden="true">${ico}</span><span class="nav-label">${label}</span><span class="sidebar-badge" data-badge="${id}" aria-hidden="true"></span></button>`
  ).join("");
  nav.querySelectorAll(".nav-btn").forEach((b) => {
    b.onclick = () => activateTab(b.getAttribute("data-view"));
  });
}

async function updateSidebarBadges(signal) {
  try {
    const j = await api("/v1/state/summary", { signal: signal ?? abortCtl.signal, bypassCache: true });
    const s = j.data || {};
    const setBadge = (viewId, text, tone) => {
      const el = document.querySelector(`[data-badge="${viewId}"]`);
      if (!el) return;
      el.textContent = text || "";
      el.classList.remove("sidebar-badge--dot", "sidebar-badge--warn", "sidebar-badge--danger");
      if (tone === "dot") el.classList.add("sidebar-badge--dot");
      else if (tone === "warn") el.classList.add("sidebar-badge--warn");
      else if (tone === "danger") el.classList.add("sidebar-badge--danger");
    };
    const ot = s.open_tasks || 0;
    setBadge("tasks", ot > 0 ? String(ot) : "", ot > 0 ? "warn" : "");
    const wu = s.waiting_user || 0;
    setBadge("escalations", wu > 0 ? "●" : "", wu > 0 ? "danger" : "");
    const pa = s.pending_approvals || 0;
    setBadge("approvals", pa > 0 ? String(pa) : "", pa > 0 ? "warn" : "");
  } catch (_) {
    /* sin token o API caída — badges vacíos */
  }
}

function activateTab(id) {
  const leaving = currentView;
  uiRenderGen += 1;
  abortCtl.abort();
  abortCtl = new AbortController();
  const signal = abortCtl.signal;
  currentView = id;
  try {
    const u = new URL(window.location.href);
    u.searchParams.set("view", id);
    history.replaceState({}, "", u.pathname + u.search + u.hash);
  } catch (_) {}
  document.querySelectorAll(".nav-btn").forEach((b) => {
    const active = b.getAttribute("data-view") === id;
    b.classList.toggle("active", active);
    if (active) b.setAttribute("aria-current", "page");
    else b.removeAttribute("aria-current");
  });
  const main = document.getElementById("main");
  if (!main) return;
  if (leaving === "chat" && main._chatPoll) {
    clearInterval(main._chatPoll);
    main._chatPoll = null;
  }
  const prev = main.getAttribute("data-prev-view");
  if (prev && prev !== id) {
    document.body.classList.remove("jmc-mode-flash");
    void document.body.offsetWidth;
    document.body.classList.add("jmc-mode-flash");
    setTimeout(() => document.body.classList.remove("jmc-mode-flash"), 720);
  }
  main.setAttribute("data-prev-view", id);
  main.dataset.jmcView = id;
  const fn = views[id];
  if (fn) _renderCatch(fn(main, signal));
  updateSidebarBadges(signal);
}

function updateSidebarFoot() {
  const el = document.getElementById("sidebar-foot-status");
  if (!el) return;
  const tok = !!getToken();
  let apiLine;
  if (!tok) apiLine = "API: sin token guardado";
  else if (lastHealthOk === null) apiLine = "API: comprobando…";
  else if (lastHealthOk) apiLine = "API: OK";
  else apiLine = "API: sin conexión";

  let diskLine;
  if (!tok || lastHealthOk !== true) diskLine = "Modo en disco: —";
  else if (lastModeWriteEnabled === null) diskLine = "Modo en disco: …";
  else if (lastModeWriteEnabled) diskLine = "Modo en disco: escribible";
  else diskLine = "Modo en disco: solo lectura";

  const full = apiLine + " · " + diskLine;
  el.textContent = full;
  el.title =
    full +
    ". Tras Guardar en Conexión el token persiste al recargar; en Modes, Aplicar escribe el modo en ~/.openclaw/.env (ver JMC_OPERACION.md).";
}

async function refreshModeWriteFromApi() {
  if (!getToken() || lastHealthOk !== true) {
    lastModeWriteEnabled = null;
    updateSidebarFoot();
    return;
  }
  const ac = new AbortController();
  try {
    const j = await api("/v1/modes/current", { bypassCache: true, signal: ac.signal });
    lastModeWriteEnabled = !!(j.data && j.data.mode_write_enabled);
  } catch {
    lastModeWriteEnabled = null;
  }
  updateSidebarFoot();
}

function updateHealthTitle() {
  const wrap = document.getElementById("health-dot");
  if (!wrap) return;
  const t = getToken();
  const b = getApiBase();
  const baseNote = b ? " (API: " + b + ")" : "";
  wrap.title = t
    ? "Estado del adapter (/v1/health). Token Bearer presente en Conexión." + baseNote
    : "Sin API o sin token: abre «Conexión» y guarda un Bearer si tu adapter exige auth para /v1/state/*. Sin token, muchas rutas devuelven 401." + baseNote;
  const conn = document.getElementById("btn-connection");
  if (conn) {
    const warn = !t || lastHealthOk === false;
    conn.classList.toggle("btn-connection--warn", warn);
    const apiTail = b ? " Origen API: " + b + "." : "";
    conn.title = warn
      ? (!t
          ? "Sin token Bearer: muchas rutas devolverán 401."
          : "El adapter no respondió a /v1/health (revisar que jmc-adapter esté en marcha).") + apiTail
      : "Conexión y polling." + apiTail;
  }
}

async function pingHealth() {
  const led = document.querySelector("#health-dot .health-led");
  const lb = document.getElementById("health-label");
  if (!led || !lb) return;
  try {
    const j = await api("/v1/health", { bypassCache: true });
    lastHealthOk = true;
    led.className = "health-led health-led--ok";
    lb.textContent = "API OK";
    applyBrandFromHealth(j.data && j.data.brand);
  } catch {
    lastHealthOk = false;
    led.className = "health-led health-led--bad";
    lb.textContent = "Sin API";
  }
  updateHealthTitle();
  void refreshModeWriteFromApi();
}

function updatePollReadout() {
  const el = document.getElementById("poll-readout");
  const poll = document.getElementById("poll");
  if (!el || !poll) return;
  const sec = Math.max(5, parseInt(poll.value, 10) || 15);
  el.textContent = `Polling ${sec}s`;
}

async function updateJmcAuthLockBanner() {
  const el = document.getElementById("jmc-auth-banner");
  if (!el) return;
  const base = getApiBase() || (typeof window !== "undefined" && window.location ? window.location.origin : "");
  if (!base) return;
  try {
    const r = await fetch(base + "/v1/auth/status", { method: "GET", headers: { Accept: "application/json" } });
    const j = await r.json();
    const d = j.data || {};
    if (d.locked) {
      el.hidden = false;
      el.textContent =
        "Auth bloqueado para esta IP (" +
        String(d.fails ?? "") +
        " fallos). Reintento en ~" +
        String(d.retry_after_sec ?? "") +
        "s.";
    } else el.hidden = true;
  } catch {
    el.hidden = true;
  }
}

function applyJmcThemeFromStorage() {
  let t = "";
  try {
    t = String(localStorage.getItem("jmc_theme_override") || "").trim();
  } catch (_) {}
  document.body.classList.remove("jmc-force-light", "jmc-force-dark");
  if (t === "light") document.body.classList.add("jmc-force-light");
  else if (t === "dark") document.body.classList.add("jmc-force-dark");
}

function schedulePoll() {
  if (pollTimer) clearInterval(pollTimer);
  const pollEl = document.getElementById("poll");
  const sec = Math.max(5, parseInt(pollEl && pollEl.value, 10) || 15);
  updatePollReadout();
  pollTimer = setInterval(async () => {
    if (pollInFlight) return;
    pollInFlight = true;
    try {
      await updateJmcAuthLockBanner();
      await pingHealth();
      await refreshAgentUiFromApi(abortCtl.signal);
      await updateGlobalNotifBadge(abortCtl.signal);
      const main = document.getElementById("main");
      const fn = views[currentView];
      if (fn && POLL_AUTO_REFRESH_VIEWS.has(currentView) && main) {
        abortCtl.abort();
        abortCtl = new AbortController();
        _renderCatch(fn(main, abortCtl.signal));
      }
      updateSidebarBadges(abortCtl.signal);
    } finally {
      pollInFlight = false;
    }
  }, sec * 1000);
}

function cmdkClose() {
  const bd = document.getElementById("cmdk-backdrop");
  if (bd) bd.hidden = true;
}

function cmdkExecute(action, arg) {
  cmdkClose();
  if (action === "tab") activateTab(arg);
  else if (action === "searchGlobal") searchGlobalOpen();
  else if (action === "export") document.getElementById("btn-export-view")?.click();
  else if (action === "clearTasks") {
    taskFilter = { status: "all", agent: "", q: "", tags: [] };
    persistFilters();
    activateTab("tasks");
  } else if (action === "clearAct") {
    actFilters = { agent: "", kind: "", tag: "", since: "", limit: 80, group: actFilters.group || "flat" };
    actCursor = null;
    persistFilters();
    activateTab("activity");
  } else if (action === "task") openTaskModal(arg);
  else if (action === "agent") {
    taskFilter.agent = arg;
    persistFilters();
    activateTab("tasks");
  }
}

function cmdkRefreshList(query) {
  const list = document.getElementById("cmdk-list");
  if (!list) return;
  const qq = String(query || "").trim().toLowerCase();
  const items = [];
  items.push({ label: "Búsqueda global en repo (Ctrl+Shift+F)", action: "searchGlobal", arg: "" });
  for (const [id, label] of NAV) {
    if (!navRoleFilter(id)) continue;
    items.push({ label: `Ir a ${label}`, action: "tab", arg: id });
  }
  items.push({ label: "Export JSON (vista actual)", action: "export", arg: "" });
  items.push({ label: "Limpiar filtros (Tasks)", action: "clearTasks", arg: "" });
  items.push({ label: "Limpiar filtros (Activity)", action: "clearAct", arg: "" });
  for (const t of tasksCacheForPalette) {
    const id = t.id;
    if (!id) continue;
    items.push({ label: `Abrir tarea ${id}`, action: "task", arg: String(id) });
  }
  const owners = [...new Set(tasksCacheForPalette.map((r) => r.owner).filter(Boolean))].sort();
  for (const o of owners) {
    items.push({ label: `Tasks: filtrar agente ${o}`, action: "agent", arg: o });
  }
  const filt = qq ? items.filter((x) => x.label.toLowerCase().includes(qq)) : items;
  const slice = filt.slice(0, 100);
  list.innerHTML = slice.length
    ? slice
        .map(
          (x) =>
            `<li><button type="button" class="cmdk-item" data-action="${escapeHtml(x.action)}" data-arg="${escapeHtml(x.arg)}">${escapeHtml(x.label)}</button></li>`
        )
        .join("")
    : '<li class="muted" style="padding:0.5rem 0.75rem">Sin coincidencias</li>';
  list.querySelectorAll(".cmdk-item").forEach((btn) => {
    btn.onclick = () => cmdkExecute(btn.getAttribute("data-action"), btn.getAttribute("data-arg"));
  });
}

function cmdkOpen() {
  const bd = document.getElementById("cmdk-backdrop");
  const inp = document.getElementById("cmdk-input");
  if (!bd || !inp) return;
  bd.hidden = false;
  inp.value = "";
  cmdkRefreshList("");
  inp.focus();
}

function showShortcutsModal() {
  showModal(`<h2 style="margin-top:0">Atajos JMC</h2>
    <ul style="font-size:0.9rem;text-align:left;margin:0.5rem 0 0;padding-left:1.2rem">
    <li><kbd>Alt</kbd>+<kbd>Shift</kbd>+<kbd>E</kbd> — Exportar JSON de la vista actual</li>
    <li><kbd>Ctrl</kbd>+<kbd>K</kbd> — Paleta de comandos</li>
    <li><kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>F</kbd> — Búsqueda global (MEMORY, docs, skills…)</li>
    <li><kbd>g</kbd> luego <kbd>j</kbd> — Jerarquía (workspace → agentes → skills)</li>
    <li><kbd>?</kbd> — Esta ayuda (no en campos de texto)</li>
    <li><kbd>Esc</kbd> — Cerrar modales o la paleta</li>
    </ul>`);
}

function setConnectionPopover(open) {
  const pop = document.getElementById("connection-popover");
  const btn = document.getElementById("btn-connection");
  if (!pop || !btn) return;
  pop.hidden = !open;
  btn.setAttribute("aria-expanded", open ? "true" : "false");
}

const st = document.getElementById("save-token");
if (st)
  st.onclick = async () => {
    const as = document.getElementById("auth-status");
    const apiInp = document.getElementById("api-base");
    const apiRaw = apiInp ? apiInp.value.trim() : "";
    if (apiRaw) {
      const nb = normalizeApiBaseUrl(apiRaw);
      if (nb === null) {
        if (as) as.textContent = "URL del API inválida (use http://host:puerto)";
        return;
      }
      localStorage.setItem(LS_API_BASE, nb);
    } else {
      localStorage.removeItem(LS_API_BASE);
    }
    apiCache.clear();
    const v = document.getElementById("token").value.trim();
    if (v) localStorage.setItem(LS_KEY, v);
    else localStorage.removeItem(LS_KEY);
    const pollEl = document.getElementById("poll");
    if (pollEl) {
      const sec = Math.max(5, Math.min(300, parseInt(pollEl.value, 10) || 15));
      try {
        localStorage.setItem(LS_POLL, String(sec));
      } catch (_) {}
    }
    if (as) {
      const apiLab = apiRaw ? "API remota" : "API = esta pestaña";
      const tokLab = v ? "con token" : "sin token";
      as.textContent = "Guardado · " + apiLab + " · " + tokLab;
    }
    updateHealthTitle();
    await pingHealth();
    activateTab(currentView);
  };

const modalClose = document.getElementById("modal-close");
if (modalClose) modalClose.onclick = hideModal;
const modalBackdrop = document.getElementById("modal-backdrop");
if (modalBackdrop)
  modalBackdrop.onclick = (e) => {
    if (e.target.id === "modal-backdrop") hideModal();
  };

const sbToggle = document.getElementById("sidebar-toggle");
if (sbToggle)
  sbToggle.onclick = () => {
    document.getElementById("sidebar").classList.toggle("open");
  };

document.addEventListener("DOMContentLoaded", () => {
  loadPersistedFilters();
  const bootParams = new URLSearchParams(window.location.search);
  const tagQ = bootParams.get("tag");
  if (tagQ) {
    actFilters.tag = tagQ;
    persistFilters();
  }
  applyUiDensity();
  applyJmcThemeFromStorage();
  document.querySelectorAll("[data-theme-pick]").forEach((b) => {
    b.onclick = () => {
      const v = b.getAttribute("data-theme-pick") || "auto";
      try {
        if (v === "auto") localStorage.removeItem("jmc_theme_override");
        else localStorage.setItem("jmc_theme_override", v);
      } catch (_) {}
      applyJmcThemeFromStorage();
    };
  });
  const forget = document.getElementById("btn-forget-token");
  if (forget) {
    forget.onclick = () => {
      try {
        localStorage.removeItem(LS_KEY);
        localStorage.removeItem("jmc_api_ok");
        apiCache.clear();
      } catch (_) {}
      const ti = document.getElementById("token");
      if (ti) ti.value = "";
      showToast("Token y caché API local limpiados.", "ok");
      void pingHealth();
    };
  }
  const t = getToken();
  const tok = document.getElementById("token");
  if (t && tok) tok.value = t;
  const apiB = document.getElementById("api-base");
  if (apiB) apiB.value = localStorage.getItem(LS_API_BASE) || "";
  buildSidebar();
  const poll = document.getElementById("poll");
  if (poll) {
    try {
      const saved = localStorage.getItem(LS_POLL);
      if (saved) {
        const n = Math.max(5, Math.min(300, parseInt(saved, 10) || 15));
        poll.value = String(n);
      }
    } catch (_) {}
    poll.addEventListener("change", () => {
      try {
        const sec = Math.max(5, Math.min(300, parseInt(poll.value, 10) || 15));
        localStorage.setItem(LS_POLL, String(sec));
      } catch (_) {}
      schedulePoll();
    });
    poll.addEventListener("input", updatePollReadout);
  }
  const btnEx = document.getElementById("btn-export-view");
  if (btnEx) {
    btnEx.onclick = () => {
      const payload = viewExportPayload[currentView];
      localStorage.setItem(LS_LAST_EXPORT, new Date().toISOString());
      updateExportHint();
      downloadJson(exportFilename("jmc-" + currentView), payload);
    };
  }
  updateExportHint();
  updatePollReadout();
  updateHealthTitle();
  updateSidebarFoot();

  const btnConn = document.getElementById("btn-connection");
  const popConn = document.getElementById("connection-popover");
  if (btnConn && popConn) {
    btnConn.onclick = () => setConnectionPopover(popConn.hidden);
    document.addEventListener(
      "click",
      (e) => {
        if (popConn.hidden) return;
        const t = e.target;
        if (btnConn.contains(t) || popConn.contains(t)) return;
        setConnectionPopover(false);
      },
      true
    );
  }

  const cmdkBd = document.getElementById("cmdk-backdrop");
  const cmdkInp = document.getElementById("cmdk-input");
  if (cmdkBd && cmdkInp) {
    cmdkBd.addEventListener("click", (e) => {
      if (e.target === cmdkBd) cmdkClose();
    });
    cmdkInp.addEventListener("input", () => cmdkRefreshList(cmdkInp.value));
  }

  document.addEventListener("keydown", (e) => {
    const tag = e.target && e.target.tagName;
    if (jmcAwaitG && tag !== "INPUT" && tag !== "TEXTAREA" && tag !== "SELECT") {
      jmcAwaitG = false;
      if (jmcAwaitGTimer) clearTimeout(jmcAwaitGTimer);
      const k = String(e.key).toLowerCase();
      const map = {
        a: "agents",
        j: "hierarchy",
        o: "overview",
        t: "tasks",
        s: "system",
        f: "files",
        m: "modes",
        h: "health_deep",
        e: "errors",
        z: "zombies",
        c: "costs",
      };
      if (map[k]) {
        e.preventDefault();
        activateTab(map[k]);
        return;
      }
    }
    if (!e.ctrlKey && !e.altKey && (e.key === "g" || e.key === "G") && tag !== "INPUT" && tag !== "TEXTAREA" && tag !== "SELECT") {
      e.preventDefault();
      jmcAwaitG = true;
      if (jmcAwaitGTimer) clearTimeout(jmcAwaitGTimer);
      jmcAwaitGTimer = setTimeout(() => {
        jmcAwaitG = false;
      }, 480);
      return;
    }
    if (e.key === "Escape") {
      cmdkClose();
      searchGlobalClose();
      setConnectionPopover(false);
      return;
    }
    if (e.ctrlKey && e.shiftKey && String(e.key).toLowerCase() === "f") {
      if (tag === "INPUT" || tag === "TEXTAREA") return;
      e.preventDefault();
      searchGlobalOpen();
      return;
    }
    if (e.ctrlKey && String(e.key).toLowerCase() === "k") {
      if (tag === "INPUT" || tag === "TEXTAREA") return;
      e.preventDefault();
      cmdkOpen();
      return;
    }
    if (e.key === "?" && tag !== "INPUT" && tag !== "TEXTAREA") {
      e.preventDefault();
      showShortcutsModal();
      return;
    }
    if (!e.altKey || !e.shiftKey || e.key.toLowerCase() !== "e") return;
    if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT") return;
    e.preventDefault();
    if (btnEx) btnEx.click();
  });

  const sbShort = document.getElementById("sidebar-shortcuts");
  if (sbShort) sbShort.onclick = () => showShortcutsModal();

  const btnNotif = document.getElementById("btn-sidebar-notif");
  if (btnNotif) btnNotif.onclick = () => openNotificationsModal();
  const btnSearchHdr = document.getElementById("btn-search-global");
  if (btnSearchHdr) btnSearchHdr.onclick = () => searchGlobalOpen();
  const sbd = document.getElementById("search-backdrop");
  const sInp = document.getElementById("search-global-input");
  if (sbd && sInp) {
    sbd.addEventListener("click", (e) => {
      if (e.target === sbd) searchGlobalClose();
    });
    sInp.addEventListener("input", () => {
      clearTimeout(searchGlobalTimer);
      const v = sInp.value;
      searchGlobalTimer = setTimeout(() => searchGlobalRun(v), 320);
    });
  }

  const bootView = bootParams.get("view");
  if (bootView && views[bootView]) activateTab(bootView);
  else activateTab("overview");
  void updateJmcAuthLockBanner();
  void pingHealth().then(() => updateGlobalNotifBadge(abortCtl.signal));
  schedulePoll();
});

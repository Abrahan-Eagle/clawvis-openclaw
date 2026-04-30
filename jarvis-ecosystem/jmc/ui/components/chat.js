/**
 * Chat JMC — burbujas y descarga de adjuntos (Bearer).
 * Requiere JMC_TABLES (escapeHtml). Carga antes de app.js.
 */
(function (global) {
  function esc(s) {
    return global.JMC_TABLES && global.JMC_TABLES.escapeHtml
      ? global.JMC_TABLES.escapeHtml(s)
      : String(s || "")
          .replace(/&/g, "&amp;")
          .replace(/</g, "&lt;")
          .replace(/>/g, "&gt;")
          .replace(/"/g, "&quot;")
          .replace(/'/g, "&#39;")
          .replace(/`/g, "&#96;");
  }

  /**
   * @param {string} convId
   * @param {Array<{ message?: object, reply?: object | null }>} rows
   */
  function renderBubbles(convId, rows) {
    const lines = [];
    for (const row of rows || []) {
      const m = row.message || {};
      const r = row.reply;
      const midRaw = String(m.id || "");
      const mid = esc(midRaw);
      const ts = esc((m.ts || "").slice(0, 19));
      const txt = esc(m.text || "");
      const atts = Array.isArray(m.attachments) ? m.attachments : [];
      const attHtml = atts.length
        ? `<div class="chat-attach-row">${atts
            .map(function (a) {
              const sn = a.stored_name || "";
              return `<button type="button" class="btn btn--ghost btn-sm chat-dl" data-conv="${esc(convId)}" data-msg="${esc(
                midRaw
              )}" data-file="${esc(sn)}" title="${esc(String(a.size_bytes || 0))} bytes" aria-label="Descargar adjunto ${esc(
                sn
              )}">⬇ ${esc(sn)}</button>`;
            })
            .join("")}</div>`
        : "";
      let inner = `<div class="chat-bubble chat-bubble--ceo"><div class="chat-bubble__meta muted">${ts} · CEO <span class="mono">${mid}</span></div><div class="chat-bubble__text">${txt.replace(
        /\n/g,
        "<br/>"
      )}</div>${attHtml}</div>`;
      if (r && typeof r === "object") {
        const rts = esc((r.ts || "").slice(0, 19));
        const rtx = esc(r.text || "");
        inner += `<div class="chat-bubble chat-bubble--jarvis"><div class="chat-bubble__meta muted">${rts} · Jarvis</div><div class="chat-bubble__text">${rtx.replace(
          /\n/g,
          "<br/>"
        )}</div></div>`;
      }
      lines.push(`<div class="chat-msg-block">${inner}</div>`);
    }
    return lines.join("");
  }

  function bindDownloads(root, getToken, getApiBase) {
    root.querySelectorAll(".chat-dl").forEach(function (btn) {
      btn.onclick = function () {
        const conv = btn.getAttribute("data-conv");
        const msg = btn.getAttribute("data-msg");
        const file = btn.getAttribute("data-file");
        const tok = getToken();
        const base = (getApiBase() || "").replace(/\/+$/, "");
        if (!conv || !msg || !file || !tok) return;
        const u =
          base +
          "/v1/chat/conversations/" +
          encodeURIComponent(conv) +
          "/messages/" +
          encodeURIComponent(msg) +
          "/attachments/" +
          encodeURIComponent(file);
        fetch(u, { headers: { Authorization: "Bearer " + tok } })
          .then(function (r) {
            if (!r.ok) throw new Error("HTTP " + r.status);
            return r.blob();
          })
          .then(function (blob) {
            const url = URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = file;
            a.click();
            setTimeout(function () {
              URL.revokeObjectURL(url);
            }, 2000);
          })
          .catch(function (e) {
            alert(e.message || "Descarga fallida");
          });
      };
    });
  }

  global.JMC_CHAT = {
    renderBubbles: renderBubbles,
    bindDownloads: bindDownloads,
  };
})(typeof window !== "undefined" ? window : globalThis);

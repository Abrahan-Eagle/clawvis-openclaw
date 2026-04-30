/**
 * Tablero tipo kanban (solo HTML; la lógica de columnas sigue en app.js).
 * Carga después de components/tables.js y antes de app.js.
 */
(function (global) {
  /**
   * @param {boolean} taskBoardHasExtraFilters
   * @param {(s: unknown) => string} escapeHtml
   * @param {string} colLabel
   */
  function emptyColumnHtml(taskBoardHasExtraFilters, escapeHtml, colLabel) {
    const esc = escapeHtml;
    if (taskBoardHasExtraFilters) {
      return (
        '<div class="kanban-empty kanban-empty--filtered">' +
        '<p class="muted">0 tareas con los filtros activos (agente, tags o búsqueda).</p>' +
        '<button type="button" class="btn btn--ghost btn-sm btn-flt-clear-board">Limpiar filtros</button>' +
        "</div>"
      );
    }
    return '<p class="muted kanban-empty">Sin tareas en ' + esc(colLabel) + ".</p>";
  }

  /**
   * @param {object} r — fila tarea
   * @param {Record<string, string>} agMap
   * @param {boolean} tagsAvailable
   * @param {string} [extraClass]
   * @param {{
   *   escapeHtml: (s: unknown) => string,
   *   badgeTask: (row: object) => string,
   *   fmtRel: (ts: unknown) => string,
   *   tagHue: (t: string) => number,
   *   taskDurationMs: (row: object) => number | null,
   *   fmtDurMs: (ms: number | null) => string,
   * }} deps
   */
  function kanbanCardHtml(r, agMap, tagsAvailable, extraClass, deps) {
    const esc = deps.escapeHtml;
    const tid = r.id || "";
    const ag = agMap[tid] || r._jmc_orphan_ag;
    const agHtml = ag ? '<span class="badge-ag">' + esc(ag) + "</span>" : "";
    const orphanNote = r._jmc_orphan_placeholder
      ? '<span class="badge badge--wait" title="No hay task JSON en state/tasks">AG sin tarea</span>'
      : "";
    let tagHtml = "";
    if (tagsAvailable && Array.isArray(r.tags) && r.tags.length) {
      tagHtml =
        '<div class="kanban-tags">' +
        r.tags
          .map(String)
          .map(function (t) {
            return (
              '<span class="tag-chip tag-chip--hue" style="--tag-hue:' +
              deps.tagHue(t) +
              'deg">' +
              esc(t) +
              "</span>"
            );
          })
          .join("") +
        "</div>";
    }
    const title = r.title || tid || "—";
    const isClosed = (r.jmc_status || "") === "closed";
    const durMs = !isClosed ? deps.taskDurationMs(r) : null;
    let durHtml = "";
    if (isClosed) {
      if (r.ended_at) {
        durHtml = '<span class="muted kanban-dur">cerrado hace ' + deps.fmtRel(r.ended_at) + "</span>";
      }
    } else {
      const dur = deps.fmtDurMs(durMs);
      if (dur && dur !== "0s") durHtml = '<span class="muted kanban-dur">' + esc(dur) + "</span>";
    }
    const dossier = r.dossier_id
      ? '<span class="mono kanban-dossier" title="dossier">' + esc(String(r.dossier_id).slice(0, 18)) + "</span>"
      : "";
    const stalled = (r.jmc_status || "") === "open" && durMs != null && durMs > 86400000 ? " kanban-card--stalled" : "";
    const orphanCls = r._jmc_orphan_placeholder ? " kanban-card--orphan" : "";
    const clickCls = r._jmc_orphan_placeholder ? "" : " click-row";
    const ex = extraClass || "";
    return (
      '<div class="kanban-card' +
      clickCls +
      " " +
      ex +
      stalled +
      orphanCls +
      '" data-task="' +
      esc(tid) +
      '">' +
      '<div class="kanban-card-title">' +
      orphanNote +
      esc(title.slice(0, 120)) +
      (title.length > 120 ? "…" : "") +
      "</div>" +
      '<div class="kanban-card-meta">' +
      deps.badgeTask(r) +
      " " +
      agHtml +
      '<span class="muted kanban-owner">' +
      esc(r.owner || "") +
      "</span> " +
      dossier +
      durHtml +
      "</div>" +
      tagHtml +
      "</div>"
    );
  }

  global.JMC_KANBAN = {
    emptyColumnHtml: emptyColumnHtml,
    kanbanCardHtml: kanbanCardHtml,
  };
})(typeof window !== "undefined" ? window : globalThis);

/**
 * Tablas de datos reutilizables (JMC UI vanilla).
 * Carga antes de app.js; expone JMC_TABLES.
 */
(function (global) {
  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;")
      .replace(/`/g, "&#96;");
  }

  /**
   * @param {Array<{ key: string, label: string }>} cols
   * @param {object[]} rows — cada fila: valores en row[col.key] (stringificados y escapados)
   * @param {{ rowClass?: (row: object) => string, rowAttrs?: (row: object) => Record<string, string> }} [opts]
   */
  function renderDataTable(cols, rows, opts) {
    const esc = escapeHtml;
    const thead = "<tr>" + cols.map(function (c) { return "<th>" + esc(c.label) + "</th>"; }).join("") + "</tr>";
    const tbody = (rows || [])
      .map(function (row) {
        const tds = cols
          .map(function (c) {
            const v = row[c.key];
            return "<td>" + (v != null && v !== "" ? esc(String(v)) : "") + "</td>";
          })
          .join("");
        let extra = "";
        if (opts && opts.rowClass) {
          const cls = opts.rowClass(row);
          if (cls) extra += ' class="' + esc(cls) + '"';
        }
        if (opts && opts.rowAttrs) {
          const attrs = opts.rowAttrs(row) || {};
          Object.keys(attrs).forEach(function (k) {
            extra += " " + esc(k) + '="' + esc(String(attrs[k] ?? "")) + '"';
          });
        }
        return "<tr" + extra + ">" + tds + "</tr>";
      })
      .join("");
    return '<table class="data"><thead>' + thead + "</thead><tbody>" + tbody + "</tbody></table>";
  }

  global.JMC_TABLES = {
    escapeHtml: escapeHtml,
    renderDataTable: renderDataTable,
  };
})(typeof window !== "undefined" ? window : globalThis);

# JARVIS-DOCUMENTS — Convención de archivos en el equipo del superusuario

**Fuente de verdad** para dónde guardar entregables, borradores y medios **fuera del repo Git**. El ecosistema Jarvis (agentes, skills) debe asumir esta estructura salvo que el humano indique otra ruta explícita.

---

## Regla absoluta

- **Única raíz permitida** para archivos de trabajo del holding: la carpeta del sistema llamada **`Documents`** (nombre en **inglés**), ruta **`~/Documents/`**. **No** usar como convención del repo la carpeta `documentos`, `Documentos` ni `~/Documentos/` — si el SO solo creó `~/Documentos/`, crea un enlace simbólico `~/Documents` → `~/Documentos` o anota la ruta real en `agents/jarvis/WORKSPACE_POLICY.md`.
- Dentro de `~/Documents/`, **una sola carpeta raíz Jarvis:** **`JARVIS-DOCUMENTS`** (con guiones, tal cual).
- **No** dispersar entregables en rutas ad hoc (`~/HoldingZonix`, `~/Escritorio/proyecto-x`, etc.) salvo orden expresa del superusuario para un caso puntual.

Ruta canónica (sustituir usuario):

```text
/home/<usuario>/Documents/JARVIS-DOCUMENTS/
```

---

## Árbol estándar

```text
JARVIS-DOCUMENTS/
├── _plantillas/              # briefs, checklists, plantillas reutilizables entre empresas
├── _referencias/             # (opcional) manuales genéricos, PDFs sin duplicar por empresa
└── empresas/
    ├── <slug-empresa>/       # ej. marketing, ventas, zonix-eats — sin espacios
    │   ├── 00_marca/         # identidad de ESA empresa (logo, paleta, voz)
    │   ├── 01_interno/     # contratos, facturas, notas internas de esa unidad
    │   ├── proyectos/        # (opcional) producto, legal, compliance — si no aplica “clientes”
    │   │   └── <nombre-proyecto>/
    │   └── clientes/         # cuentas B2B gestionadas por esa empresa
    │       └── <dossier_id-o-slug-cliente>/
    │           ├── 01_borradores/
    │           ├── 02_por_aprobar/
    │           ├── 03_aprobados/
    │           └── 04_publicados/
    └── <otra-empresa>/
        └── ...
```

- **`slug-empresa`:** debe ser coherente con [../COMPANIES.md](../COMPANIES.md) cuando exista registro (ej. `marketing`, `ventas`).
- **Cliente:** preferir el mismo **`dossier_id`** que en `client-dossiers/*.json` (ej. `cli-20260404-cliente-tests-redes`).

---

## Carpeta por entrega (posts, campañas, piezas)

Dentro del flujo del cliente (p. ej. `02_por_aprobar`), **una subcarpeta por pieza**, con fecha y versión:

```text
2026-04-15_ig_feed_promo-v1/
    copy.md           # texto, hashtags (o titulo.txt si se separa)
    notas.md          # Trello, feedback, pendientes
    imagenes/
    video/
    flyers/
```

Revisiones: `..._v2`, `..._v3`.

---

## Relación con el repo

- **`jarvis-ecosystem/`** guarda **contexto estable**: dossiers JSON, briefs en Markdown, gobierno.
- **Medios pesados** (vídeo, PSD, exports grandes) viven bajo **`JARVIS-DOCUMENTS`**, no en Git.
- Si hace falta referencia desde el repo, usar **ruta relativa al home** o texto tipo: “entregables en `~/Documents/JARVIS-DOCUMENTS/empresas/marketing/clientes/<dossier_id>/...`”.

---

## Política de agentes

1. Al generar o pedir guardar un archivo de entrega, **proponer o usar** la ruta bajo `~/Documents/JARVIS-DOCUMENTS/` según empresa + cliente + estado.
2. **Leer** `agents/jarvis/WORKSPACE_POLICY.md` para rutas permitidas en esta máquina (debe incluir `JARVIS-DOCUMENTS`).
3. Si el humano contradice esta convención con una ruta concreta, **prevalece la orden del humano**.

---

## Historial

- **2026-04-04:** Convención acordada con el superusuario; documento creado para el ecosistema Jarvis.
- **2026-04-04:** Árbol inicial creado en esta máquina en `/home/aipp/Documents/JARVIS-DOCUMENTS/`: empresas `marketing` y `ventas`; bajo marketing, cliente de prueba `cli-20260404-cliente-tests-redes` con estados `01`–`04`. Verificación: [VERIFICACION_JARVIS_DOCUMENTS.md](VERIFICACION_JARVIS_DOCUMENTS.md).
- **2026-04-04:** Arbol re-verificado/asegurado en disco (`mkdir -p`); texto de verificación actualizado para usar `~` y ruta ejemplo.
- **2026-04-04:** Aclarado nombre canónico de carpeta del sistema: **`Documents`** (`~/Documents/`), no `documentos` / `Documentos` / `~/Documentos/`.

# Prompts de prueba para jarvis-ecosystem (todas las categorías)

Colección **copy-paste** para verificar el ecosistema por capas: smoke del repo, ClawFlows/OpenClaw, coordinación, pipeline RRSS, skills globales, enrutamiento de modelo, automatizaciones y gobierno (AG). La raíz de trabajo habitual es `/var/www/clawvis-openclaw/jarvis-ecosystem` (o el clon equivalente); el toplevel Git del monorepo suele ser `clawvis-openclaw`.

**Reglas comunes para todos los prompts:** no publicar contenido en redes ni APIs de pago sin aprobación; no volcar `.env` ni secretos; documentar salida en `out/PRUEBAS_<nombre>_<fecha>.md` con tabla **Prueba | Resultado | Notas** y un solo **siguiente paso** si algo falla.

**Referencias cruzadas:** [CLAWFLOWS.md](../CLAWFLOWS.md), [automations/README.md](../automations/README.md), [COORDINACION_AGENTES.md](COORDINACION_AGENTES.md), [APPROVAL_GATES.md](APPROVAL_GATES.md).

---

## 1. Smoke del repositorio y configs (base)

```
Eres verificador del ecosistema Jarvis. cd a /var/www/clawvis-openclaw/jarvis-ecosystem.

1) git status -sb y git rev-parse --show-toplevel (indicar si el toplevel es el monorepo padre).
2) python3: json.load de openclaw.json y entities.json (sin imprimir cuerpos).
3) PyYAML: mempalace.yaml
4) Recorre templates/**/*.json y automations/*.yaml (solo raíz de automations/) con validación sintáctica.
5) readlink -f client-dossiers

Escribe out/ con fecha, tabla resumen, comandos y extractos. Separa "fallo de entorno" vs "fallo del repo".
```

---

## 2. ClawFlows (Node 20 + registry)

```
En jarvis-ecosystem: nvm use 20; source scripts/clawflows-env.sh; ./scripts/clawflows-verify-registry.sh.

Optional: nvm use 20 && npx --yes clawflows --version (si falla con Node 22, documenta como esperado, ver CLAWFLOWS.md sección Node 22).
```

---

## 3. OpenClaw CLI (PATH no interactivo)

```
En jarvis-ecosystem: source scripts/openclaw-path.sh; opcional OPENCLAW_NODE_VERSION=22. Luego openclaw --version y openclaw status. No interpretes 1008/gateway como fallo del árbol del repo. Documenta avisos (WhatsApp WARN, Composio, etc.) como entorno.
```

---

## 4. Diagnóstico Composio (red)

```
./scripts/composio-diagnose.sh. Esperado: HTTP 401 o similar anónimo; DNS/TLS OK. No pegues tokens.
```

---

## 5. Alineación de automatizaciones (raíz vs subcarpeta)

```
diff -q automations/jarvis-morning-briefing.yaml automations/jarvis/morning-briefing.yaml
Repite el patrón para otras copias listadas en automations/README.md si el equipo lo pide. Si difieren, propón cp desde la canónica en subcarpeta hacia la raíz según README.
```

---

## 6. Model router (jarvis, 3 perfiles de entrada)

```
Desde jarvis-ecosystem, tres ejecuciones de node agents/jarvis/scripts/model-router.mjs --json con textos: (1) "hola", (2) brief largo de marketing 80+ palabras, (3) descripción de bug con stack. Tabla: entrada | tier | agentId | matchedRule. Sin leer .env.
```

---

## 7. Coordinación: activity-log (ciclo de tarea)

```
Usa skills/global/activity-log/bin/activity-log con la API real: start requiere --agent y --title; opcional --dossier, --ref, --task. Crea tarea; registra un event (si aplica) con --payload-file mínimo vía jq; end con --task y --note. Valida state/tasks/<id>.json y activity-log jsonl. No uses flags inventados (task-id vs --task, etc.).

Referencias: docs/COORDINACION_AGENTES.md, agents/marketing/SOUL.md.
```

---

## 8. Coordinación: handoff (crear, listar, aceptar)

```
handoff: create con --from --to --schema --task --payload-file. Usa un schema mínimo con campos requeridos (p. ej. producer-to-publisher: asset_path, format, channels array). luego list --open, show, accept --id. Si falla validación, corrige el JSON contra skills/global/handoff/schemas/. Documenta handoff_id.
```

---

## 9. Coordinator (vista de pulso)

```
coordinator status; coordinator summary --dossier <id_demo>. Sin datos sensibles; solo resumen.
```

---

## 10. Memory store (estructura JSON por agente)

```
Ejecuta memory-store (ver SKILL.md) con operaciones de lectura/append según documentación; no borrar memory.json de producción sin copia. Usa un agente de prueba o ruta bajo /tmp si el skill lo permite. Si el skill requiere paths fijos, solo dry-run o cat de schema.
```

---

## 11. Brand kit

```
brand-kit: lee client-dossiers/<cli-demo>/brand.json o el symlink resuelto. Valida claves mínimas para colores y fuentes. Sin subir nada.
```

---

## 12. Pipeline carrusel (sin IA o con IA)

```
carousel-render: validate y render --out-dir a out/TEST-.../ con --no-ai primero. Opcional: sin --no-ai (recuerda aviso AG-13 y red externa). Revisa index.json (slides_count, sha, ai_used).
Ruta template típica: templates/carousels/cli-DEMO-rrss/5-errores-marketing.json
```

---

## 13. image-render (slide suelto)

```
image-render slide: --brand a client-dossiers/.../brand.json, --slide JSON de una slide, --format 1080x1920, --out out/TEST-.../slide-01.png. Doc: skills/image-render/SKILL.md
```

---

## 14. image-ai-free (Pollinations, requiere red + AG-13)

```
Solo con aprobación explícita: image-ai-free generate con prompt y aspect ratio. Cache local bajo state/cache si aplica. Anota límites de servicio gratuito.
```

---

## 15. TTS (edge-tts)

```
tts-free: venv bajo skills/tts-free; synthesize de una frase corta a out/TEST/; con --with-subs. Verifica mp3 y srt no vacío. Requiere AG-13 para uso publicable.
```

---

## 16. Subtitles (SRT/ASS)

```
subtitles: split-words o to-ass con brand; entrada desde la salida tts. Salida a out/TEST.
```

---

## 17. video-compose (reel)

```
video-compose: validate y opcional render con reel.json de demo; --task-id opcional para activity-log. Comprueba con ffprobe index.json. Doc: REELS_TIKTOK_PIPELINE_FREE.md, AG-12/13 si publicar.
```

---

## 18. Planner / task-queue / executor (secuencia seca)

```
Ejecuta planner, task-queue o executor con subcomandos de ayuda o dry-run según SKILL.md; no ejecutes acciones destructivas. Si requiere archivos, usa prefijo out/TEST-...
```

---

## 19. Skills de información (red local permitida)

```
weather-report: una ciudad fija; youtube-transcript: URL pública de prueba corta. Respeta allowlists y coste (gratis). Documenta fallos de terceros.
```

---

## 20. browser-playwright (allowlist + AG-11)

```
Solo con dominio en BROWSER_PLAYWRIGHT_ALLOW o dry-run. No navegar bancos ni login real. Probar "help" o ruta mínima documentada en SKILL.
```

---

## 21. Error recovery / activity loops (orquestación en seco)

```
Lee automations/jarvis/loop-orchestrator.yaml y explica en prosa el flujo; opcional: clawflows run ... --dry-run si Node 20 + env cargado. No asumas ejecución real del gateway.
```

---

## 22. Revisión de gobierno (solo lectura)

```
Abre docs/APPROVAL_GATES.md y documenta en tabla qué AG aplicaría a: publicar reel, voz TTS, imagen generativa, cambiar openclaw.json. No pidas aprobación real; es checklist de caja negra.
```

---

## 23. Batería "todo en uno" (mega prompt)

```
Batería en una sola sesión, en orden: (1) sección 1 smoke, (2) secciones 2-4, (3) 5, (4) 6, (5) 7-9 coordinación mínima con IDs de tarea únicos, (6) 11-13 sin publicar, (7) mega-tabla y un solo siguiente paso. Si un paso requiere red y falla, marca N/A y sigue. Salida: out/PRUEBAS_JARVIS_COMPLETO_<fecha>.md
```

---

## Dónde guardar informes

- Directorio recomendado: `jarvis-ecosystem/out/` con prefijos claros (por ejemplo `ECOSYSTEM_TEST_BLOCK_<fecha>.md`, `PRUEBAS_JARVIS_COMPLETO_<fecha>.md`).

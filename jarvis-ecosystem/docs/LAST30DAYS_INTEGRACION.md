# last30days — Inteligencia reciente (integracion abr 2026)

Skill **last30days-openclaw** (adaptacion OpenClaw del proyecto MIT [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill)): investiga un tema en los **ultimos ~30 dias** en Reddit, X, YouTube, HN, Polymarket, GitHub, web, etc., y sintetiza un brief puntuado por **engagement real** (upvotes, actividad), no solo SEO.

**Ubicacion en el repo:** [`agents/jarvis/skills/last30days-openclaw/`](../agents/jarvis/skills/last30days-openclaw/) (versionado para replica desde Git).

## Convencion con el resto del ecosistema

| Sistema | Rol |
|---------|-----|
| **MemPalace** | Memoria semantica + KG (decisiones, clientes, holding) |
| **Graphify** | Mapa estructural del repo (archivos y enlaces) |
| **last30days** | Pulso externo: que dice la comunidad **ahora** sobre un tema o persona |

No sustituyen entre si.

## Cuando usarlo en Jarvis

- **sales-hunter / lead-research-ops:** antes de contactar o calificar un lead importante: tema tecnico del proyecto, empresa, o persona publica (`python3 scripts/openclaw_run.py "TEMA"` desde el skill).
- **proposal-ops:** opcional para anclar win themes en dolores/lenguaje reciente de la comunidad.
- **mkt-content:** tendencias y preguntas frecuentes sobre un tema de contenido.

## Fuentes utiles vs ruido para este holding

| Priorizar | Usar con moderacion / opcional |
|-----------|--------------------------------|
| Reddit, HN, GitHub | TikTok, Instagram (B2B ligero) |
| Web, X (si hay sesion) | Polymarket (salvo contexto de prediccion/actualidad) |

## Instalacion y actualizacion

**Desde ClawHub (recomendado):**

```bash
cd /ruta/al/jarvis-ecosystem
openclaw skills install last30days-openclaw
```

Si `last30days-official` responde 429 (rate limit), reintentar mas tarde o usar el paquete **last30days-openclaw** (ya probado).

**Setup motor (una vez por maquina):**

```bash
cd jarvis-ecosystem/agents/jarvis/skills/last30days-openclaw
./scripts/setup_openclaw_env.sh
python3 scripts/last30days.py --diagnose
```

Secretos opcionales: `~/.openclaw/workspace/.secrets/last30days.env` (ver SKILL.md del skill).

## Ejecucion rapida (one-shot)

Desde el directorio del skill (ver [SKILL.md](../agents/jarvis/skills/last30days-openclaw/SKILL.md)):

```bash
python3 scripts/openclaw_run.py "TEMA O PERSONA"
```

Equivalente documentado en upstream:

```bash
python3 scripts/last30days.py "TEMA" --emit=compact --no-native-web
```

## Documentacion upstream

- Repo original: https://github.com/mvanhorn/last30days-skill  
- Adaptacion OpenClaw empaquetada: skill instalado incluye `UPSTREAM_README.md` y `ATTRIBUTION.md`.

# video-short — videos animados con Remotion (opcional)

**Tipo:** skill local (Node + Remotion).
**Bin:** `skills/video-short/bin/video-short`.
**Estado:** v0.5 esqueleto (Fase 4 de [PROPUESTA_MEJORA_JARVIS_V2.md](../../docs/PROPUESTA_MEJORA_JARVIS_V2.md)). Para 90% de casos, usar [`video-compose`](../video-compose/SKILL.md) (ffmpeg) que es mas rapido y simple.

---

## Cuando usar este skill

- Necesitas **animaciones tipo motion graphics** (text reveal kinetico, scroll programatico, transformaciones complejas).
- Tienes **graficos / charts** que quieres componer programaticamente.
- Necesitas **JSX** + componentes React reusables para series de videos.

## Cuando NO usarlo

- Para slides + voz + subtitulos quemados ya es suficiente [`video-compose`](../video-compose/SKILL.md). Mucho menos peso (sin Node deps), mas rapido.
- Si no quieres mantener una toolchain de Node + npm 200MB.

## Setup (una vez)

```bash
cd /var/www/clawvis-openclaw/jarvis-ecosystem/skills/video-short/remotion
npm install            # ~200MB node_modules, ~3 min primera vez
npm run dev            # studio en :3000 para diseñar templates
```

`remotion/node_modules/` y `remotion/out/` estan en `.gitignore`.

## Comandos

```bash
video-short render \
  --template five-bullets \
  --props /tmp/props.json \
  --out out/cli-DEMO-rrss/reel-anim/reel.mp4

video-short list-templates
video-short studio        # arranca remotion studio (dev)
```

## Template de prueba: `five-bullets`

Acepta `props.json`:

```json
{
  "brand_id": "cli-DEMO-rrss",
  "title": "5 errores en marketing organico",
  "bullets": [
    "Postear sin escuchar",
    "Vender en cada post",
    "Ignorar metricas",
    "Cambiar de tono",
    "Olvidar el CTA"
  ],
  "voice_audio": "out/cli-DEMO-rrss/reel-test/voice.mp3"
}
```

Render: 1080x1920 H.264 + AAC, ~3-8 min para 30s de video en CPU sin GPU.

## Limites honestos

- Remotion 4.x requiere Node 18+ y Chromium headless (~150MB extra). Si la maquina no lo tiene, hay que `npx puppeteer browsers install chrome` o setear `PLAYWRIGHT_CHANNEL` (esto se gestiona en setup).
- Tiempos: render mucho mas lento que ffmpeg porque renderiza frame-by-frame en headless Chrome.
- Curva de aprendizaje: requiere conocimiento de React/JSX para crear plantillas nuevas.

**Recomendacion:** dejar este skill para casos puntuales. Para produccion masiva de Reels usar `video-compose`.

## Plantillas previstas

| Slug | Descripcion | Duracion target |
|---|---|---|
| `five-bullets` | hook + 5 bullets + CTA, animacion text-reveal | 45s |
| `quote-card` | cita grande con autor + ambient bg | 15s |
| `step-by-step` | pasos numerados con animacion suave | 60s |

Estado: definidas, pendiente implementar JSX. Issue tracker en LESSONS.md cuando se aborde.

## AG-13

Si la voz es IA (`tts-free`) o hay assets generados por IA, requiere AG-13. Documentar en el manifiesto.

## Test rapido

```bash
cd /var/www/clawvis-openclaw/jarvis-ecosystem
skills/video-short/bin/video-short list-templates
```

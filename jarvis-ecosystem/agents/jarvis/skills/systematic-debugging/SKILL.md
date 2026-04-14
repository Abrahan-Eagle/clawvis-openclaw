---
name: systematic-debugging
description: "Usar ante CUALQUIER problema tecnico del ecosistema: gateway caido, integracion rota, script que falla, heartbeat que no ejecuta. Root cause ANTES de intentar arreglar."
---

# Debugging sistematico

Inspirado en superpowers:systematic-debugging. Adaptado al ecosistema Jarvis/OpenClaw.

## Ley de hierro

```
NINGUN FIX SIN INVESTIGACION DE ROOT CAUSE PRIMERO
```

Si no completaste la Fase 1, no puedes proponer fixes.

## Cuando usar

Ante CUALQUIER problema tecnico:
- Gateway no responde
- Heartbeat no ejecuta
- Integracion (Discord, Telegram, WhatsApp) desconectada
- Script falla
- MemPalace no indexa
- Sesion de agente no inicia
- ClawFlow no se ejecuta

Usar ESPECIALMENTE cuando:
- Bajo presion de tiempo
- "Un fix rapido" parece obvio
- Ya intentaste multiples fixes
- El fix anterior no funciono

## Las cuatro fases

### Fase 1: Investigacion de root cause

ANTES de intentar CUALQUIER fix:

1. **Leer mensajes de error completos**
   - No saltarse errores ni warnings
   - Leer stack traces completos
   - Anotar lineas, archivos, codigos de error

2. **Reproducir consistentemente**
   - Pasa cada vez? Solo a veces?
   - Cuales son los pasos exactos?

3. **Verificar cambios recientes**
   - Que cambio que podria causar esto?
   - `git diff`, commits recientes
   - Cambios en openclaw.json, .env, dependencias

4. **Recolectar evidencia en cada capa**
   ```bash
   # Capa 1: Systemd
   systemctl --user status openclaw-gateway

   # Capa 2: Logs del gateway
   journalctl --user -u openclaw-gateway --since "1 hour ago" --no-pager

   # Capa 3: Puertos
   ss -ltnp | grep 18789

   # Capa 4: Config
   jq '.gateway' ~/.openclaw/openclaw.json

   # Capa 5: Canales
   openclaw channels status --probe 2>/dev/null
   ```

5. **Trazar flujo de datos** — donde se origina el valor incorrecto? Rastrear hacia atras hasta la fuente.

### Fase 2: Analisis de patrones

1. **Buscar ejemplos funcionales** — algo similar que SI funciona?
2. **Comparar contra referencia** — leer docs de OpenClaw completos, no hacer skim
3. **Identificar diferencias** — listar TODA diferencia entre lo que funciona y lo que no
4. **Entender dependencias** — que necesita este componente para funcionar?

### Fase 3: Hipotesis y prueba

1. **Formar una sola hipotesis** — "Creo que X es el root cause porque Y"
2. **Probar minimamente** — el cambio MAS pequeno posible para testear la hipotesis
3. **Verificar antes de continuar** — funciono? Si -> Fase 4. No -> nueva hipotesis.
4. **Si no sabes** — decir "No entiendo X". No pretender saber.

### Fase 4: Implementacion

1. **Implementar un solo fix** — para el root cause identificado
2. **Verificar fix** — con verificacion-before-completion
3. **Si el fix no funciona y ya van 3+ intentos** — PARAR. Cuestionar la arquitectura. Discutir con el CEO.

## Problemas comunes del ecosistema Jarvis

| Problema | Donde investigar primero |
|----------|--------------------------|
| Gateway no inicia | `journalctl --user -u openclaw-gateway`; verificar puerto 18789 libre |
| Heartbeat no ejecuta | `openclaw.json` -> verificar bloque `heartbeat` en `agents.list[]`; HEARTBEAT.md no vacio |
| Discord no responde | `openclaw channels status --probe`; verificar token en secrets |
| MemPalace timeout | `systemctl --user status mempalace-auto-mine.timer`; verificar Ollama corriendo |
| Script falla | Ejecutar manualmente con `bash -x script.sh` para ver cada paso |
| ClawFlow no corre | `source scripts/clawflows-env.sh && clawflows check <nombre>` |
| Sesion no arranca | Verificar `agents.list[]` en openclaw.json; workspace existe? |

## Banderas rojas — PARA y vuelve a Fase 1

- "Fix rapido y despues investigo"
- "Solo cambio X a ver si funciona"
- "Multiples cambios a la vez, despues corro tests"
- "Probablemente es X, deja lo arreglo"
- "No entiendo completamente pero esto podria funcionar"
- "Un intento mas" (cuando ya intentaste 2+)

## Racionalizaciones

| Excusa | Realidad |
|--------|----------|
| "El problema es simple" | Problemas simples tienen root causes. El proceso es rapido para bugs simples. |
| "Emergencia, no hay tiempo" | Debugging sistematico es MAS RAPIDO que guess-and-check. |
| "Primero intento esto" | El primer fix establece el patron. Hazlo bien desde el inicio. |
| "Multiples fixes a la vez ahorran tiempo" | No puedes aislar que funciono. Causa nuevos bugs. |

## Referencia rapida

| Fase | Actividades | Criterio de exito |
|------|------------|-------------------|
| 1. Root Cause | Leer errores, reproducir, verificar cambios, recolectar evidencia | Entender QUE y POR QUE |
| 2. Patron | Buscar ejemplos funcionales, comparar | Identificar diferencias |
| 3. Hipotesis | Formar teoria, probar minimamente | Confirmada o nueva hipotesis |
| 4. Implementacion | Crear test/verificacion, fix, verificar | Bug resuelto, verificado |

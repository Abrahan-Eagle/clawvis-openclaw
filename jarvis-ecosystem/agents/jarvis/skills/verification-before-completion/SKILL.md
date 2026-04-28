---
name: verification-before-completion
description: "OBLIGATORIO antes de declarar cualquier tarea como completada. Ejecuta el comando/accion de verificacion, lee el resultado, y SOLO entonces afirma que esta listo. Evidencia antes de claims."
metadata:
  version: "1.0.0"
---

# Verificacion antes de completar

Inspirado en superpowers:verification-before-completion. Adaptado al ecosistema Jarvis.

## Ley de hierro

```
NINGUN CLAIM DE COMPLETADO SIN EVIDENCIA FRESCA DE VERIFICACION
```

Si no ejecutaste el comando de verificacion en este mismo turno, no puedes afirmar que funciona.

## La puerta de verificacion

```
ANTES de cualquier claim de exito o satisfaccion:

1. IDENTIFICAR: Que comando o accion prueba este claim?
2. EJECUTAR: Correr el comando completo (fresco, no cache)
3. LEER: Output completo, exit code, contar errores
4. VERIFICAR: El output confirma el claim?
   - Si NO: Reportar estado real con evidencia
   - Si SI: Hacer el claim CON evidencia
5. SOLO ENTONCES: Declarar completado

Saltarse cualquier paso = mentir, no verificar
```

## Tabla de verificacion por tipo de tarea

| Claim | Requiere | NO es suficiente |
|-------|----------|------------------|
| Script funciona | Output del script: exit 0, resultado esperado | "Deberia funcionar", "el codigo se ve bien" |
| Pipeline actualizado | Screenshot o lista de Trello mostrando tarjetas movidas | "Ya lo actualice" sin mostrar |
| Propuesta enviada | Confirmacion de envio (email, Workana, plataforma) | "La envie" sin evidencia |
| Campana publicada | URL del post o screenshot del contenido publicado | "Ya esta en redes" |
| Gateway funcionando | `systemctl --user status openclaw-gateway` mostrando active | "Lo reinicie" |
| Config aplicada | `diff` entre config esperada y actual; o `jq` query mostrando valor | "Edite el archivo" |
| Heartbeat activo | Log del gateway mostrando heartbeat tick | "Lo configure en openclaw.json" |
| Commit hecho | `git log -1 --oneline` mostrando el commit | "Hice commit" |
| Push a GitHub | `git status` mostrando "up to date with origin" | "Hice push" |
| Dossier creado | `ls client-dossiers/` mostrando el archivo | "Lo cree" |

## Banderas rojas — PARA

- Usar "deberia", "probablemente", "parece que"
- Expresar satisfaccion antes de verificar ("Listo!", "Perfecto!", "Hecho!")
- Hacer commit/push sin verificar que tests/linters pasen
- Confiar en reportes de subagentes sin verificar independientemente
- Pensar "solo esta vez" puedo saltarme la verificacion
- Estar cansado y querer terminar rapido

## Racionalizaciones comunes

| Excusa | Realidad |
|--------|----------|
| "Deberia funcionar ahora" | EJECUTA la verificacion |
| "Estoy seguro" | Confianza != evidencia |
| "Solo esta vez" | Sin excepciones |
| "El agente dijo que funciona" | Verifica independientemente |
| "Ya lo hice antes" | Verificacion anterior no cuenta; necesitas fresca |
| "Es un cambio trivial" | Cambios triviales rompen cosas. Verifica. |

## Patrones correctos

**Scripts:**
```
CORRECTO: [Ejecutar script] [Ver: exit 0, output esperado] "Script funciona"
INCORRECTO: "Deberia funcionar" / "El codigo se ve correcto"
```

**Trello:**
```
CORRECTO: [Listar tarjetas] [Ver: tarjeta en columna correcta] "Pipeline actualizado"
INCORRECTO: "Ya movi la tarjeta"
```

**Config:**
```
CORRECTO: [jq '.agents.list[0].heartbeat.every' openclaw.json] [Ver: "30m"] "Heartbeat configurado"
INCORRECTO: "Edite el archivo con el valor correcto"
```

## Sizing de verificacion

No todas las tareas requieren el mismo nivel de verificacion. Escalar segun impacto:

| Tier | Criterio | Verificacion |
|------|----------|-------------|
| **Pequena** | <5 items, un solo agente, sin impacto externo | Verificacion rapida: un comando, un check |
| **Estandar** | 5-20 items, un agente, impacto moderado | Verificacion completa: todos los items de la tabla |
| **Grande** | >20 items, cross-agent, impacto en cliente | Verificacion exhaustiva: cada item + revision independiente |

### Secuencia de verificacion para tareas grandes

```
1. BUILD / CONFIG -- el cambio se aplico correctamente
2. TEST / SCRIPT -- los scripts/procesos corren sin error
3. LINT / FORMAT -- no hay errores de formato o estructura
4. FUNCTIONALITY -- la funcionalidad esperada existe y responde
5. TODO / TASKS -- no quedan items pendientes
6. CROSS-CHECK -- un segundo agente o el CEO verifica
```

Para tareas pequenas, basta con los pasos 1 y 4.

## Regla de frescura

```
EVIDENCIA VIEJA NO CUENTA
```

- La verificacion debe ser de **este turno/sesion**, no de una sesion anterior
- Si paso mas de 5 minutos desde la verificacion y hubo cambios intermedios, RE-VERIFICAR
- Output de un subagente cuenta solo si se verifica independientemente
- "Lo verifique ayer" NO es evidencia fresca

## Cuando aplicar

SIEMPRE antes de:
- Cualquier variacion de claim de exito/completado
- Cualquier expresion de satisfaccion
- Mover tarjeta en Trello a "Done"
- Reportar al CEO que algo esta listo
- Marcar tarea como completada en TodoWrite
- Pasar a la siguiente tarea

## Linea final

**Sin atajos para verificacion.** Ejecuta el comando. Lee el output. ENTONCES declara el resultado. No negociable.

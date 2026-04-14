# Heartbeat — Jarvis (agente maestro)

Goal: G-J01 (orquestar sin intervencion constante) + G-J02 (memoria al dia).

## Checklist (ejecutar en orden, saltar si ya se hizo en <30 min)

1. **Estado del ecosistema** — Verificar que el gateway esta corriendo (`systemctl --user is-active openclaw-gateway`). Si no, reportar alerta.
2. **Trello rapido** — Revisar si hay tarjetas vencidas o sin mover en >48h en los boards activos. Si hay, resumir.
3. **Memoria** — Revisar si hay `memory/YYYY-MM-DD.md` de hoy. Si no hay nada relevante pendiente, HEARTBEAT_OK.
4. **Pipeline ventas** — Preguntar internamente si sales-hunter tiene leads sin seguimiento >24h (solo si hay datos recientes).
5. **MemPalace sync** — Si el auto-mine no corrio en >1h (revisar log si es posible), anotar.

## Reglas

- Horario activo: 08:00-24:00 America/Caracas.
- Si no hay nada que hacer: `HEARTBEAT_OK`.
- No enviar mensajes al CEO a menos que haya algo accionable.
- Cada 3 dias: revisar y consolidar MEMORY.md (limpiar entradas obsoletas).

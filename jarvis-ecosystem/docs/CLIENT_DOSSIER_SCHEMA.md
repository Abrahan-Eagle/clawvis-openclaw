# Esquema mínimo: dossier de cliente (contexto para Jarvis)

**Propósito:** un registro **estable por cliente** (organización que contrata servicios) para que la IA y el equipo **no mezclen** contextos (p. ej. cliente A = marketing, cliente B = programación).

**Ubicación sugerida:** una página Notion, carpeta en el workspace, tarjeta-madre en Trello, o archivo en `agents/jarvis/memory/` / repo bajo `client-dossiers/` — siempre con **`dossier_id` inmutable** una vez publicado.

**Última revisión:** abril 2026.

---

## Identificador

| Campo | Tipo | Obligatorio | Notas |
|-------|------|-------------|--------|
| `dossier_id` | string | Sí | Formato recomendado: `cli-YYYYMMDD-slug` o UUID. **No** reutilizar para otro cliente. |
| `version` | string | No | Semver o fecha `YYYY-MM-DD` del último cambio estructural. |

---

## Datos de negocio

| Campo | Tipo | Obligatorio | Notas |
|-------|------|-------------|--------|
| `nombre_comercial` | string | Sí | Nombre con el que se referencia al cliente. |
| `rubro` | string | Sí | A qué se dedica (ej. retail, SaaS, restauración). |
| `descripcion_actividad` | string | No | Párrafo corto: qué hace el cliente. |
| `contacto_principal` | object | No | `nombre`, `email`, `telefono` (sin datos sensibles innecesarios en repos compartidos). |

---

## Servicios y planificación

| Campo | Tipo | Obligatorio | Notas |
|-------|------|-------------|--------|
| `servicios_contratados_o_deseados` | array de string | Sí | Ej. `["marketing_digital"]`, `["desarrollo_software"]`, `["diseno"]`. |
| `empresa_del_holding_asignada` | string | No | ID o nombre corto de la unidad (ej. `marketing`, `dev_agency`). |
| `objetivos` | array de string | No | Resultados esperados medibles cuando sea posible. |
| `planificacion_resumen` | string | No | Hitos, fases o backlog de alto nivel acordado con el cliente. |
| `nivel_servicio_o_notas_comerciales` | string | No | SLA, horario, restricciones. |

---

## Historial para la IA

| Campo | Tipo | Obligatorio | Notas |
|-------|------|-------------|--------|
| `decisiones_relevantes` | array de {fecha, texto} | No | Decisiones que Jarvis no debe “olvidar” al planificar. |
| `enlaces` | array de {titulo, url} | No | Contratos en drive, board Trello, canal Discord del proyecto (si aplica). |

---

## Ejemplo JSON mínimo

```json
{
  "dossier_id": "cli-20260404-acme",
  "version": "2026-04-04",
  "nombre_comercial": "ACME C.A.",
  "rubro": "Comercio minorista",
  "descripcion_actividad": "Cadena regional de ferretería; foco en presencia digital 2026.",
  "servicios_contratados_o_deseados": ["marketing_digital", "gestion_redes"],
  "empresa_del_holding_asignada": "marketing",
  "objetivos": ["Calendario editorial Q2", "Campaña local Valencia"],
  "planificacion_resumen": "Fase 1 auditoría; Fase 2 contenidos; Fase 3 ads.",
  "decisiones_relevantes": [
    { "fecha": "2026-04-01", "texto": "Prioridad Instagram sobre TikTok hasta nuevo aviso." }
  ]
}
```

## Ejemplo alternativo (solo programación)

```json
{
  "dossier_id": "cli-20260404-beta-dev",
  "nombre_comercial": "Beta Labs",
  "rubro": "Startup fintech",
  "servicios_contratados_o_deseados": ["desarrollo_software", "mantenimiento"],
  "empresa_del_holding_asignada": "dev_agency",
  "objetivos": ["API v2 en producción antes de julio"],
  "planificacion_resumen": "Sprint actual: auth + webhooks."
}
```

---

## Uso con Jarvis

Al iniciar un tema sobre un cliente, el superusuario puede indicar: **`dossier_id`** o pegar el JSON/path del archivo. Jarvis debe tratar ese bloque como **fuente de verdad** para ese cliente hasta que se actualice el dossier.

Ver también [GOBIERNO_JARVIS_V2.md](GOBIERNO_JARVIS_V2.md) y [CONVENCION_TRELLO_EMPRESA_CLIENTE.md](CONVENCION_TRELLO_EMPRESA_CLIENTE.md) para enlazar tarjetas al mismo `dossier_id`.

# Recursos comunidad OpenClaw / Claude Code (curado para Jarvis)

**Ámbito:** inventario **externo** al monorepo `clawvis-openclaw`; sirve para **descubrir** plantillas, skills y patrones sin obligar a instalarlos.  
**Última revisión:** abril 2026.

---

## 1. Hallazgo forense (qué hay en este repo vs fuera)

| Ámbito | En `jarvis-ecosystem` | Fuera (comunidad) |
|--------|----------------------|-------------------|
| Gobierno multi-empresa | [GOBIERNO_JARVIS_V2.md](GOBIERNO_JARVIS_V2.md), Trello, dossiers | No sustituible por un “framework” genérico; los enlaces siguientes son **complemento opcional**. |
| Skills por agente | Carpetas `agents/*/skills/` (convención del workspace) | [openclaw/skills](https://github.com/openclaw/skills), listas awesome (abajo). |
| Automatización real | ClawFlows, gateway OpenClaw, credenciales en host | Repos de demos/uso; validar permisos y privacidad antes de copiar. |

**Conclusión:** nada de la lista siguiente **reemplaza** a Jarvis como orquestador del holding; como mucho **enriquece** plantillas (SOUL), skills puntuales o metodología de trabajo en repos de código.

---

## 2. Criterios de adopción (obligatorio antes de instalar)

1. **Licencia:** MIT/BSD preferible; AGPL/Commons Clause implica revisar redistribución y uso comercial.
2. **Datos:** skills que envíen contenido a terceros o scrapeen redes — revisar ToS y política del cliente.
3. **Operación:** evitar servicios 24/7 obligatorios salvo que el superusuario los quiera mantener.
4. **Alineación:** debe poder mapearse a **empresa + dossier + Trello** sin romper [FLUJO_TRELLO_ECOSISTEMA.md](FLUJO_TRELLO_ECOSISTEMA.md).

---

## 3. Inventario por categoría (enlaces)

### Núcleo y frameworks

| Recurso | URL | Nota para Jarvis |
|---------|-----|------------------|
| OpenClaw (upstream) | https://github.com/openclaw/openclaw | Referencia de producto; alinear versiones con el gateway del host. |
| Clade (multi-agente Markdown) | https://github.com/satoh-y-0323/clade | Útil como **idea** de fases con aprobación humana en **proyectos Claude Code**; no mergear el framework entero en el monorepo sin necesidad. |
| Claude Code | https://github.com/anthropics/claude-code | Base CLI; Clade y muchos skills asumen su presencia. |
| Stokowski (Symphony) | https://github.com/Sugar-Coffee/stokowski | Aislamiento de agentes; evaluar solo si hace falta sandbox fuerte. |

### Plantillas y agentes

| Recurso | URL | Nota |
|---------|-----|------|
| Awesome OpenClaw Agents | https://github.com/mergisi/awesome-openclaw-agents | Plantillas SOUL; inspiración para marketing/ventas; no copiar ciegamente identidades ya definidas en el holding. |
| OpenClaw Agents Kit | https://github.com/shenhao-stu/openclaw-agents | Despliegue rápido de flota; contrastar con `COMPANIES.md` y roles por empresa. |

### Skills y registro

| Recurso | URL | Nota |
|---------|-----|------|
| Awesome OpenClaw Skills | https://github.com/VoltAgent/awesome-openclaw-skills | Catálogo grande; filtrar por categoría e instalar **pocos** skills revisados. |
| OpenClaw Official Skills | https://github.com/openclaw/skills | Registro público oficial. |
| Xiaohongshu Skills | https://github.com/white0dew/XiaohongshuSkills | Solo si el ICP incluye esa plataforma. |
| Reddit Growth Skill | https://github.com/oh-ashen-one/reddit-growth-skill | Solo si marketing prioriza Reddit. |

### Casos de uso y GTM

| Recurso | URL | Nota |
|---------|-----|------|
| Awesome OpenClaw Use Cases | https://github.com/hesamsheikh/awesome-openclaw-usecases | Ideas de playbooks; documentación de referencia. |
| Markster OS (GTM B2B) | https://github.com/markster-public/markster-os | Lenguaje GTM en chat; revisar prompts; no dependencia obligatoria. |

### Patrones de trabajo (recomendado para tareas grandes de código)

| Recurso | URL | Nota |
|---------|-----|------|
| Three Man Team | https://github.com/russelleNVy/three-man-team | Patrón **Arquitecto → Constructor → Revisor** (MIT); encaja con dev-agency y cambios grandes; ver [GOBIERNO_JARVIS_V2.md](GOBIERNO_JARVIS_V2.md) sección ampliada. |

### Monitoreo y RL (baja prioridad por defecto)

| Recurso | URL | Nota |
|---------|-----|------|
| OpenClaw Office | https://github.com/WW-AI-Lab/openclaw-office | UI “oficina”; requiere servicio adicional. |
| OpenClaw-RL | https://github.com/Gen-Verse/OpenClaw-RL | RL sobre agentes; complejidad alta; solo I+D explícito. |

---

## 4. Qué no hacer desde Jarvis sin decisión explícita

- Instalar **decenas** de skills a la vez (ruido, conflictos, mantenimiento).
- Sustituir **Trello + dossier** por herramientas solo-chat sin trazabilidad.
- Incorporar repos **AGPL/Commons** en productos comerciales sin asesoría legal.

---

## 5. Referencias internas

- Gobierno: [GOBIERNO_JARVIS_V2.md](GOBIERNO_JARVIS_V2.md)
- Integraciones gateway: [INTEGRACIONES_OPENCLAW_YA_CONFIGURADAS.md](INTEGRACIONES_OPENCLAW_YA_CONFIGURADAS.md)
- Flujo Kanban: [FLUJO_TRELLO_ECOSISTEMA.md](FLUJO_TRELLO_ECOSISTEMA.md)

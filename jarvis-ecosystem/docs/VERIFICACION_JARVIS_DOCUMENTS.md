# Verificación — JARVIS-DOCUMENTS en el PC

**Objetivo:** comprobar que existe la carpeta canónica de entregables bajo `~/Documents/` y el subárbol mínimo para las empresas activas del holding.

**Convención:** [JARVIS_DOCUMENTS_ON_DISK.md](JARVIS_DOCUMENTS_ON_DISK.md).

**Última ejecución (referencia):** 2026-04-04 — árbol creado en `/home/aipp/Documents/JARVIS-DOCUMENTS/` para `marketing`, `ventas` y cliente de prueba `cli-20260404-cliente-tests-redes`.

---

## Comandos rápidos

```bash
# Debe existir la raíz
test -d ~/Documents/JARVIS-DOCUMENTS && echo OK || echo FALTA

# Listar primer nivel
ls -la ~/Documents/JARVIS-DOCUMENTS

# Árbol (si tienes tree)
tree -d -L 5 ~/Documents/JARVIS-DOCUMENTS 2>/dev/null || find ~/Documents/JARVIS-DOCUMENTS -type d | sort
```

---

## Checklist mínimo (empresas activas)

Sustituir `<usuario>` si no es `aipp`:

| Ruta esperada | Contenido |
|---------------|-----------|
| `~/Documents/JARVIS-DOCUMENTS/_plantillas/` | Plantillas globales |
| `~/Documents/JARVIS-DOCUMENTS/_referencias/` | Referencias genéricas (opcional) |
| `~/Documents/JARVIS-DOCUMENTS/empresas/marketing/00_marca/` | Marca de la empresa marketing |
| `~/Documents/JARVIS-DOCUMENTS/empresas/marketing/01_interno/` | Interno marketing |
| `~/Documents/JARVIS-DOCUMENTS/empresas/marketing/clientes/` | Cuentas B2B |
| `~/Documents/JARVIS-DOCUMENTS/empresas/ventas/00_marca/` | Marca ventas |
| `~/Documents/JARVIS-DOCUMENTS/empresas/ventas/01_interno/` | Interno ventas |
| `~/Documents/JARVIS-DOCUMENTS/empresas/ventas/clientes/` | Cuentas (vacío hasta nuevos dossiers) |

**Cliente de prueba (marketing):** `.../marketing/clientes/cli-20260404-cliente-tests-redes/` con `01_borradores`, `02_por_aprobar`, `03_aprobados`, `04_publicados`.

---

## Política del agente

Las rutas absolutas en esta máquina figuran en [../agents/jarvis/WORKSPACE_POLICY.md](../agents/jarvis/WORKSPACE_POLICY.md).

Si falta la carpeta, crear el árbol según [JARVIS_DOCUMENTS_ON_DISK.md](JARVIS_DOCUMENTS_ON_DISK.md) o repetir el procedimiento documentado en el historial de ese archivo.

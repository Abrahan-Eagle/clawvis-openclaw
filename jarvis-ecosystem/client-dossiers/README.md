# Dossiers de cliente

Cada archivo en este directorio representa a **un cliente** (organizacion que contrata servicios a una o mas empresas del holding).

**Esquema de campos:** [../docs/CLIENT_DOSSIER_SCHEMA.md](../docs/CLIENT_DOSSIER_SCHEMA.md).  
**Gobierno operativo:** [../docs/GOBIERNO_JARVIS_V2.md](../docs/GOBIERNO_JARVIS_V2.md).

---

## Convenciones

| Regla | Detalle |
|-------|---------|
| **Formato** | JSON (`.json`). Un archivo por cliente. |
| **Nombre del archivo** | Igual al `dossier_id`: `cli-YYYYMMDD-slug.json`. |
| **`dossier_id` inmutable** | Una vez publicado, no reutilizar para otro cliente. |
| **Campos obligatorios** | `dossier_id`, `nombre_comercial`, `rubro`, `servicios_contratados_o_deseados`. |
| **Sin datos sensibles** | No guardar contrasenas, tokens ni datos financieros completos en el repo. |
| **Entregables y medios en el PC** | No van en Git; usar `~/Documents/JARVIS-DOCUMENTS/` con la misma empresa y `dossier_id` que el JSON. Ver [../docs/JARVIS_DOCUMENTS_ON_DISK.md](../docs/JARVIS_DOCUMENTS_ON_DISK.md). |

---

## Cliente de prueba (ecosistema)

Para **depurar** flujos (Jarvis, marketing, Trello, Discord) sin datos reales:

| dossier_id | Archivos |
|------------|----------|
| `cli-20260404-cliente-tests-redes` | [cli-20260404-cliente-tests-redes.json](cli-20260404-cliente-tests-redes.json), [BRIEF_CLIENTE_TESTS_REDES.md](BRIEF_CLIENTE_TESTS_REDES.md) |

Marcado como cliente ficticio en `decisiones_relevantes` del JSON. No usar credenciales Meta reales en el repo.

---

## Como usa Jarvis estos dossiers

1. Al iniciar un tema sobre un cliente, el superusuario indica el `dossier_id` o pega el path del archivo.
2. Jarvis lee el JSON como **fuente de verdad** para ese cliente durante la sesion.
3. Si el superusuario pide trabajo sobre un cliente y no existe dossier, Jarvis propone crearlo aqui con los campos minimos.
4. Los dossiers se enlazan desde Trello (etiqueta o prefijo `[dossier_id]`) y desde los canales Discord del proyecto.

---

## Crear un dossier nuevo

**Plantilla minima (campos vacios):** [cli-PLANTILLA-vacio.json](cli-PLANTILLA-vacio.json).

```bash
cp cli-PLANTILLA-vacio.json cli-YYYYMMDD-nuevo-slug.json
# Editar dossier_id y todos los campos con datos reales
```

**Ejemplo relleno (referencia):** [cli-20260404-ejemplo.json](cli-20260404-ejemplo.json).

Tras crear un dossier real, actualizar la tabla **Clientes activos** en [../agents/jarvis/MEMORY.md](../agents/jarvis/MEMORY.md).

O pedir a Jarvis: _"Crea un dossier para [nombre del cliente] que quiere [servicios]"_.

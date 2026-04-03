# Scripts auxiliares

| Script | Proposito |
|--------|-----------|
| [`clawflows-env.sh`](clawflows-env.sh) | Exporta `CLAWFLOWS_DIR`, `CLAWFLOWS_REGISTRY` y `CLAWFLOWS_SKILLS` usando `npm root -g` (sin rutas fijas a una version de Node). Uso: `source .../scripts/clawflows-env.sh` |
| [`clawflows-verify-registry.sh`](clawflows-verify-registry.sh) | Ejecuta `clawflows check` para cada YAML en `automations/registry/` (requiere `clawflows-capability-map`). Omite `lead-qualifier` con mensaje (sin `metadata.json` remoto). |
| [`validate-lead-qualifier-local.sh`](validate-lead-qualifier-local.sh) | Comprueba `curl` y `jq` en PATH para la automatizacion `lead-qualifier`. |

# client-onboard

**Tipo:** skill global ejecutable.  
**Bin:** `skills/global/client-onboard/bin/client-onboard`  
**Estado:** v1 (loop RRSS P0)

```bash
client-onboard init --id nuevo-cliente --nombre "Acme" --instagram @acme
client-onboard brand --dossier nuevo-cliente
client-onboard checklist --dossier nuevo-cliente
```

Crea `client-dossiers/<id>/dossier.json` + `brand.json`. Tokens Meta **nunca** en git — solo checklist `accesos_meta`.

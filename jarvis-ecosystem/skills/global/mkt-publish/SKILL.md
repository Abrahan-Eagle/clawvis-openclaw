# mkt-publish

**Tipo:** skill global ejecutable.  
**Bin:** `skills/global/mkt-publish/bin/mkt-publish`  
**Estado:** v1 (dry-run + Meta Graph IG opcional)

```bash
mkt-publish --handoff handoff-... --dry-run
mkt-publish --handoff handoff-... --force-live   # requiere approval-gate approved + META_* env
```

## Credenciales (solo en HOME / env, nunca git)

| Variable | Uso |
|----------|-----|
| `META_ACCESS_TOKEN` | Graph API |
| `META_IG_USER_ID` | Instagram Business |
| `META_ASSET_PUBLIC_URL` | URL pública de la imagen (Graph no acepta file://) |
| `META_PAGE_ID` | Facebook Page (parcial) |

**TikTok / X / LinkedIn:** documentados como **manual** en v1.  
Log: `state/publish-log/pub-*.json`.

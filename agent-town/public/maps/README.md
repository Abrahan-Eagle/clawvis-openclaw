# Mapas Tiled (`public/maps/`)

Los JSON exportados desde Tiled deben referenciar **rutas relativas** bajo `public/` (p. ej. `../tilesets/*.png` desde este directorio). `office2.json` / `office2.tmx` ya usan solo `public/tilesets/`; los PNG no van en git — véase [`../tilesets/README.md`](../tilesets/README.md).

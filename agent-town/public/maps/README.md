# Mapas Tiled (`public/maps/`)

Los JSON exportados desde Tiled deben referenciar **rutas relativas** bajo `public/` (p. ej. tilesets en `public/tilesets/`). Si un `.json` aún apunta a carpetas de otro usuario o a `~/Pictures/...`, reexporta el mapa en Tiled tras copiar los assets al repo.

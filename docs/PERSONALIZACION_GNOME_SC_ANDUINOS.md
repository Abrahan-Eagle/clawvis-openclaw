# Personalización GNOME / AnduinOS (estilo tutorial SC)

Referencia del estado actual y mantenimiento.

## Estado actual (resumen)

| Área | Configuración |
|------|----------------|
| Shell | `Marble-yellow-dark` (tema [Marble](https://github.com/imarkoff/Marble-shell-theme)) |
| Iconos | `bloom-dark` (Deepin, en `~/.local/share/icons/`) |
| Cursor | `Afterglow-cursors` |
| Dock | Dash to Dock (izquierda); Dash to Panel no está en uso |
| Hanabi | Vídeo de fondo; audio del vídeo **silenciado** (`mute=true`); pausa con ventana maximizada/pantalla completa en ambos monitores (`pause-on-maximize-or-fullscreen=2`) |
| Icono Hanabi en barra | Tema del sistema `preferences-desktop-wallpaper-symbolic` (edición en `panelMenu.js`) |

**Extensiones desactivadas a propósito (más liviano / menos distracción):**

- **Burn My Windows** — efectos al abrir/cerrar ventanas.
- **Sound Visualizer** — barras de audio en el escritorio.

**Vídeo de ejemplo:** `~/Videos/wallpapers/sample-live-wallpaper.mp4` (sustituible por cualquier `.mp4`).

## Rendimiento y fluidez

1. **Hanabi (live wallpaper)**  
   - Usa GPU; con **autopausa** al maximizar/fullscreen se reduce mucho el uso en juegos o trabajo a pantalla completa.  
   - Vídeos **1080p o menos** y bitrate moderado consumen menos que 4K.  
   - **Mute** evita decodificar audio innecesario.  
   - Si el vídeo va a tirones: en preferencias de Hanabi prueba **Force GtkMediaFile** o revisa drivers NVIDIA (según [Hanabi](https://github.com/jeffshee/gnome-ext-hanabi) y caché GStreamer).

2. **Blur My Shell**  
   - Añade coste de composición; si notas tirones, baja el blur en su configuración o desactívalo temporalmente.

3. **Muchas extensiones**  
   - Cada extensión añade JS en el shell. Si hace falta aligerar: desactiva primero las **puramente decorativas** (p. ej. RunCat, Coverflow Alt-Tab) y prueba de nuevo.

4. **Caché GStreamer (opcional)**  
   - Si hay fallos raros de vídeo: `rm -rf ~/.cache/gstreamer-1.0/` (se regenera sola). No hace falta borrarla en el día a día.

5. **Recargar el shell tras cambios gordos**  
   - X11: `Alt+F2` → `r` → Enter. Wayland: cerrar sesión.

## Dependencias del sistema

Meson y cava pueden instalarse con apt si los necesitas en el PATH global:

```bash
sudo apt update && sudo apt install -y meson cava
```

## Restaurar barra tipo Windows (Dash to Panel)

En **Gestor de extensiones**: desactivar **Dash to Dock** y activar **Dash to Panel** (`dash-to-panel@jderose9.github.com`).

## Archivos tocados (Hanabi)

- `~/.local/share/gnome-shell/extensions/hanabi-extension@jeffshee.github.io/panelMenu.js` — icono del panel.  
- `~/.local/share/gnome-shell/extensions/hanabi-extension@jeffshee.github.io/hanabi-symbolic.svg` — respaldo / alternativa (el panel usa icono de tema).

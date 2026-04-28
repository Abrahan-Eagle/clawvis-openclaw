# weather-report

> Patrón inspirado en la idea de clima por coordenadas (MK37 `weather_report.py`); **implementación propia** vía [Open-Meteo](https://open-meteo.com/) — sin clave.

## Uso

```bash
chmod +x bin/weather-report   # una vez
./bin/weather-report
./bin/weather-report --lat 40.4 --lon -3.7 "Madrid"
```

Variables opcionales: `WEATHER_DEFAULT_LAT`, `WEATHER_DEFAULT_LON`.

## Salida

JSON con `label`, `lat`, `lon`, `current` (temperatura, humedad, `weather_code` WMO, viento) y `source: open-meteo`.

## Integración

- Morning brief: ver `automations/jarvis/morning-briefing.yaml` (paso con `fetch` / notify).
- CLI local o `exec` en OpenClaw con ruta absoluta al script.

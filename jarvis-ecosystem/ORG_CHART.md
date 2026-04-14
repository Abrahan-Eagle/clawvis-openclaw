# Organigrama del holding Jarvis

Representacion visual de la jerarquia operativa. Fuente: [COMPANIES.md](COMPANIES.md).

---

```mermaid
graph TD
    CEO["Abrahan Pulido<br/>(Superusuario / CEO del holding)"]

    CEO --> Jarvis["jarvis<br/>Agente maestro / Orquestador<br/>Goal: G-J01, G-J02"]

    Jarvis --> MktEmpresa["Marketing & Comunicacion<br/>(Empresa activa)"]
    Jarvis --> VentasEmpresa["Ventas<br/>(Empresa activa)"]
    Jarvis --> DevAgency["Dev-Agency<br/>(Planificada)"]
    Jarvis --> Legal["Legal<br/>(Planificada)"]
    Jarvis --> Contadores["Contadores<br/>(Planificada)"]

    MktEmpresa --> mkt_content["mkt-content<br/>Contenido y copywriting<br/>Goal: G-M01"]
    MktEmpresa --> mkt_social["mkt-social<br/>Gestion de redes sociales<br/>Goal: G-M01"]
    MktEmpresa --> mkt_analytics["mkt-analytics<br/>Analitica y reportes<br/>Goal: G-M02"]
    MktEmpresa --> mkt_ads["mkt-ads<br/>Publicidad paga<br/>Goal: G-M01"]
    MktEmpresa --> mkt_email["mkt-email<br/>Email marketing<br/>Goal: G-M02"]

    VentasEmpresa --> sales_hunter["sales-hunter<br/>Prospeccion y leads<br/>Goal: G-V01"]
    VentasEmpresa --> sales_closer["sales-closer<br/>Cierre de ventas<br/>Goal: G-V01"]
    VentasEmpresa --> sales_account["sales-account<br/>Gestion de cuentas<br/>Goal: G-V02"]
```

---

## Leyenda

- **Linea solida**: reporta a / es orquestado por.
- **Goal: G-XXX**: meta principal del agente (ver [GOALS.md](GOALS.md)).
- **Empresas planificadas**: sin agentes ni workspace activos; se crearan cuando el CEO lo autorice.

## Actualizacion

Al agregar agentes o empresas, actualizar este diagrama y [COMPANIES.md](COMPANIES.md) simultaneamente.

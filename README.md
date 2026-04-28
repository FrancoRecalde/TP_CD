# TPI Ciencia de Datos — UTN FRC 2026
## Grupo 15 | 5K4

Dataset: **PAMAP2 Physical Activity Monitoring**  
Fuente: [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/231/pamap2+physical+activity+monitoring)  
Licencia: CC BY 4.0

---

## Estructura del repositorio

```
.
├── data/
│   ├── raw/          # Archivos .dat originales (NO incluidos — ver descarga)
│   ├── processed/    # CSV consolidado tras ETL
│   └── external/     # Fuentes externas adicionales
├── notebooks/
│   └── 01_ETL.ipynb  # ETL + EDA — Entrega 2
├── reports/
│   └── entrega_2/    # Informe PDF + figuras exportadas
├── src/              # Helpers y funciones reutilizables
└── README.md
```

---

## Descarga del dataset

Los archivos `.dat` originales no están en este repositorio (≈500 MB en total).

**Opción A — Desde UCI directamente:**
```bash
# Descargar desde https://archive.ics.uci.edu/dataset/231/pamap2+physical+activity+monitoring
# Extraer y colocar los archivos subject101.dat ... subject109.dat en data/raw/Protocol/
# Colocar los archivos opcionales en data/raw/Optional/
```

**Opción B — Desde Google Drive del grupo:**  
_(link compartido internamente)_

---

## Hipótesis del proyecto

| ID | Hipótesis | Tipo |
|----|-----------|------|
| H1 | Clasificar tipo de actividad física desde señales inerciales + HR | Clasificación multiclase |
| H2 | Distinguir actividades de baja movilidad (sitting, standing, watching TV) | Clasificación supervisada |
| H3 | Predecir nivel de esfuerzo (bajo/medio/alto) desde señales IMU | Clasificación con feature engineering |

---

## Integrantes

| Rol | Nombre | Legajo |
|-----|--------|--------|
| Product Owner | Franco Recalde | 94661 |
| Scrum Master | Emilio Sadir | — |
| Team | (6 integrantes restantes) | — |

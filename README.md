# Analítica de Datos - PC1

Proyecto grupal orientado a la obtención (web scraping), limpieza/análisis exploratorio (EDA) y visualización de datos sobre Seguridad Ciudadana.

## Objetivos
1. Recolectar datos desde fuentes web (públicas o semi estructuradas).
2. Estandarizar y limpiar la información para análisis.
3. Generar indicadores y visualizaciones.
4. Presentar resultados en una interfaz (ej. Streamlit).

## Estructura del Proyecto
```
├── config.yaml              # Configuración general
├── requirements.txt         # Dependencias
├── .env.sample              # Variables de entorno ejemplo
├── data/
│   ├── raw/                 # Datos crudos (no modificar manualmente)
│   ├── interim/             # Datos intermedios / transformaciones parciales
│   ├── processed/           # Datos listos para análisis / modelo
│   └── external/            # Datos externos suplementarios
├── src/
│   ├── main.py              # Punto de entrada de la app (Streamlit)
│   ├── data_collection/     # Scripts de scraping / ingestión
│   ├── eda/                 # Funciones de análisis exploratorio
│   ├── app/                 # Layout y componentes UI
│   └── utils/               # Utilidades (logging, paths, helpers)
├── notebooks/               # Notebooks de exploración (no código de producción)
├── tests/                   # Tests simples / smoke tests
└── docs/                    # Documentación adicional
```

## Flujo de Trabajo (Pipeline Conceptual)
1. Scraping / Ingesta: Guardar archivos originales en `data/raw`.
2. Limpieza y normalización: Resultados a `data/interim`.
3. Feature engineering / dataset final: Guardar en `data/processed`.
4. Carga en la interfaz para visualización (gráficos, tablas, KPIs).

## Instalación Rápida
Requiere Python 3.10+.

```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.sample .env
```

## Ejecutar la Aplicación (Streamlit)
```bash
streamlit run src/main.py
```

## Convenciones
- Código productivo en `src/`.
- No subir datos sensibles ni crudos pesados (ya ignorados por `.gitignore`).
- Notebooks: nombrar con prefijo incremental: `01_exploracion_inicial.ipynb`.
- Funciones reutilizables deben migrarse desde notebooks a módulos en `src/`.

## Tests
Ejecutar smoke test:
```bash
python -m pytest -q
```

## Próximos Pasos Sugeridos
- Implementar scraping real (requests + parsing HTML/JSON).
- Añadir limpieza robusta (tipos, nulos, outliers).
- Crear visualizaciones (Streamlit + Altair/Plotly).
- Añadir perfilado de datos (ydata-profiling opcional).
- Definir métricas clave de Seguridad Ciudadana.

## Autores
Equipo del curso - PC1.

---
> Mantener este README actualizado a medida que evoluciona el pipeline.

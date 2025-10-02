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

## Tecnologías Principales
- **Análisis y Procesamiento de Datos**: `pandas`
- **Recolección de Datos (Scraping)**: `requests`
- **Visualizaciones Interactivas**: `plotly`
- **Aplicación Web Interactiva**: `streamlit`
- **API para Visualizaciones**: `fastapi`

## Instalación Rápida
Requiere Python 3.10+.

```bash
# 1. Crear y activar un entorno virtual
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar variables de entorno
cp .env.sample .env
```
Después de copiar, edita el archivo `.env` y añade tu token de Mapbox. Este token es necesario para generar las visualizaciones de mapas.

## Ejecución

El proyecto tiene tres componentes principales que se pueden ejecutar de forma independiente:

### 1. Pipeline de Recolección de Datos

Este script se encarga de descargar los datos de denuncias en paralelo. Es el primer paso y el más importante para obtener la información.

```bash
python scripts/ejecutar_todos_v2.py
```

Los archivos se guardarán en la carpeta `data_v2/`.

### 2. Aplicación de Visualización (Streamlit)

La aplicación interactiva permite explorar los datos procesados. Asegúrate de haber ejecutado el pipeline de EDA primero.

```bash
streamlit run src/main.py
```

### 3. API de Visualización (FastAPI)

Expone visualizaciones como archivos HTML a través de endpoints. Útil para integrar los mapas en otras webs.

```bash
uvicorn src.api.main:app --reload
```

La API estará disponible en `http://127.0.0.1:8000`.

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

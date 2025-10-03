# Analítica de Datos - Seguridad Ciudadana (PC1)

Proyecto para recolectar, depurar, analizar y visualizar denuncias de seguridad ciudadana (fuente ArcGIS / MININTER) mediante un pipeline reproducible.

## 📌 Objetivos
1. Ingesta de datos (scraping / API) y almacenamiento crudo.
2. Limpieza y estandarización reproducible (pipeline modular).
3. Validación y consolidación en un dataset final (`denuncias_final.csv`).
4. Generación de visualizaciones interactivas (HTML Plotly) sin acoplar lógica a la presentación.
5. (Opcional) Exponer el dataset / HTML vía FastAPI.

## 🧭 Flujo General
Ingesta → Limpieza / Transformación → Dataset Final → Visualizaciones → (Opcional) API.

| Etapa | Entrada | Salida | Carpeta |
|-------|---------|--------|---------|
| Ingesta | Servicios ArcGIS | Datos crudos (CSV / JSON / GeoJSON) | `data/raw/` |
| Limpieza / Intermedio | Raw | Tablas depuradas parciales | `data/interim/` |
| Procesado final | Interim | `denuncias_final.csv` | `data/processed/` |
| Visualización | Processed | Gráficos / mapas HTML | `reports/visualizations/` |
| API (opcional) | Processed / HTML | Endpoints de entrega | `src/api/` |

## 🗂️ Estructura Principal
```
requirements.txt              # Dependencias del entorno
.env.sample                   # Variables de entorno de ejemplo
config/
  config.yaml                 # Parámetros generales (paths, scraping, logging)
  scraping_periods.yaml       # (Opcional) definición de periodos/años a ingestar
data/
  raw/                        # Datos crudos (no modificar manualmente)
  interim/                    # Datos intermedios (pasos de limpieza)
  processed/                  # Dataset(s) finales (ej. denuncias_final.csv)
  external/                   # (Opcional) datos externos complementarios
docs/
  architecture.md
  data_dictionary.md
  eda_history/                # Reportes y narrativa de EDA histórica
notebooks/
  01_limpieza_exploracion.ipynb  # Exploración; la lógica estable vive en src/
reports/
  visualizations/             # ÚNICA carpeta de artefactos HTML finales
scripts/
  run_ingestion.py            # Ejecuta solo ingesta
  run_processing.py           # Ejecuta limpieza / transformación
  run_visualizations.py       # Genera todas las visualizaciones
  run_full_pipeline.py        # Orquesta extremo a extremo
src/
  api/                        # (Opcional) Endpoints FastAPI mínimos
    main.py
  ingestion/                  # Lógica de descarga parametrizada
    fetch.py
    periods.py
  processing/                 # Limpieza, transformación y validaciones
    clean.py
    transform.py
    validate.py
  visualization/              # Generación de gráficos (Plotly)
    build_charts.py
    maps.py
    run_all.py
  utils/                      # Utilidades compartidas
    logger.py
    paths.py
    config.py
tests/                        # (Sugerido) pruebas unitarias / de esquema
```

### Principios
- Código ≠ Artefactos: `src/` contiene únicamente lógica Python reutilizable.
- Artefactos (HTML finales y CSV procesados) se generan fuera de `src/`.
- Notebook sólo para exploración; reproducibilidad garantizada por scripts.
- Ingesta parametrizada (sin proliferación de archivos por periodo).
- Visualizaciones reproducibles con un comando.

## 🧪 Requisitos
| Recurso | Versión recomendada |
|---------|----------------------|
| Python  | 3.10+                |
| SO      | Linux / macOS / Windows |

## ⚙️ Instalación Rápida
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
cp .env.sample .env               # Luego editar .env
```

## 🔐 Variables de Entorno (.env)
| Variable | Descripción | Obligatorio |
|----------|-------------|-------------|
| MAPBOX_TOKEN | Token para mapas (Plotly/Mapbox) | Sí (para mapas) |
| APP_ENV | entorno (dev/prod) | No |
| LOG_LEVEL | Nivel logging (INFO/DEBUG) | No |

Si no se usa Mapbox, los mapas que lo requieran no se renderizarán correctamente.

## 🏗️ Configuración (`config.yaml`)
Define rutas base y parámetros de scraping (user agent, timeout). Se puede extender para añadir límites de tasa, proxies, etc.

## 🚀 Ejecución de Componentes
### 1. Ingesta
```bash
python scripts/run_ingestion.py
```
Lee periodos (si existen) desde `config/scraping_periods.yaml`.

### 2. Procesamiento / Limpieza
```bash
python scripts/run_processing.py
```
Genera/actualiza `data/interim/` y `data/processed/denuncias_final.csv`.

### 3. Visualizaciones
```bash
python scripts/run_visualizations.py
```
Genera HTML en `reports/visualizations/`.

### 4. Pipeline completo
```bash
python scripts/run_full_pipeline.py
```

### 5. API (opcional)
```bash
uvicorn src.api.main:app --reload
```
Sirve dataset final o gráficos (si se requiere) en http://127.0.0.1:8000

### 6. Pruebas (si existen)
```bash
pytest -q
```

## 📊 Visualizaciones
Política:
- Única carpeta de salida: `reports/visualizations/`.
- No duplicar archivos en `src/api/templates/` (evitar HTML pesados allí).
- Nombrado en snake_case: `barras_top_delitos.html`, `heatmap_hora_dia.html`, etc.
- Variantes usar sufijos: `_filtrada`, `_detalle`.

### Servir visualizaciones por API (opcional)
```python
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI()
VIZ_DIR = Path(__file__).resolve().parents[2] / "reports" / "visualizations"

@app.get("/viz/{archivo}")
def get_viz(archivo: str):
	fp = VIZ_DIR / archivo
	if not fp.exists():
		raise HTTPException(404, "No encontrado")
	return FileResponse(fp)
```

### Recomendación de .gitignore
Si los HTML se pueden regenerar:
```
reports/visualizations/
!reports/visualizations/README.md
```

## 🧱 Logger
Configurado en `src/utils/logger.py`. Ajustar nivel mediante variable de entorno (`LOG_LEVEL`) o entrada en `config/config.yaml`.

## 🧪 Calidad / Buenas Prácticas
- Ingesta parametrizada (un solo módulo + configuración).
- Lógica pura modular (import seguro, sin efectos colaterales).
- Rutas relativas con `pathlib.Path` + centralización en `config/` y `utils/paths.py`.
- Validación de esquema antes de exportar dataset final (pandera/pydantic recomendado).
- Reproducibilidad: artefactos grandes pueden excluirse del control de versiones.

## ❗ Problemas Frecuentes
| Situación | Causa | Solución |
|-----------|-------|----------|
| Mapas no cargan | Falta `MAPBOX_TOKEN` | Añadir token en `.env` |
| Descarga lenta / timeout | Límite servidor ArcGIS | Reducir ventana temporal o paginar por fecha |
| Error GeoJSON → fallback JSON | Endpoint no soporta geometría directa | Se maneja automáticamente en scripts `codigo_*.py` |
| Rutas Windows en Linux | Hardcode previo | Editar scripts y usar `os.path.join` / `pathlib.Path` |

## 🔮 Próximos Pasos (Roadmap sugerido)
- Consolidar refactor (eliminar scripts legacy duplicados si persisten).
- Añadir validación de esquema (`processing/validate.py`).
- Implementar caché incremental (solo periodos nuevos).
- Generar solo visualizaciones seleccionadas vía flags / CLI.
- Automatizar con pre-commit + CI (lint, tests, generación selectiva).

## 🤝 Contribuir
1. Crear rama (`feature/nombre-feature`).
2. Añadir/actualizar tests si aplica.
3. Ejecutar `pytest -q` antes de hacer push.
4. Abrir PR con descripción clara del cambio.

## 👥 Autores
Equipo del curso - PC1. Uso académico / demostrativo.

---
Mantener este README alineado con el estado real del pipeline.

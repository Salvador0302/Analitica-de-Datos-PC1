# Analítica de Datos - Seguridad Ciudadana (PC1)

Proyecto académico/grupal para recolectar, depurar, analizar y visualizar denuncias de seguridad ciudadana (fuente ArcGIS / MININTER) mediante un pipeline reproducible y una capa de presentación (Streamlit + API FastAPI).

## 📌 Objetivos
1. Ingesta de datos (scraping / API) y almacenamiento bruto.
2. Limpieza, estandarización y enriquecimiento (EDA sistematizado).
3. Generación de datasets procesados y visualizaciones interactivas.
4. Exposición vía aplicación web y endpoints reutilizables.

## 🧭 Visión Rápida del Flujo
Scraping → Limpieza/Transformación → Dataset Final → Visualizaciones (HTML / App) → API / Consumo externo.

| Etapa | Entrada | Salida | Carpeta |
|-------|---------|--------|---------|
| Ingesta | Servicios ArcGIS | CSV/GeoJSON crudo | `data/raw` |
| Limpieza / Intermedio | Raw | Tablas depuradas parciales | `data/interim` |
| Procesado final | Interim | Dataset listo (ej. `denuncias_final.csv`) | `data/processed` |
| Visualización | Processed | Mapas / Gráficos HTML | `reports/visualizations/` + `src/api/templates/` |
| App / API | Processed + HTML | UI interactiva / Endpoints | `src/main.py` / `src/api/` |

## 🗂️ Estructura Principal
```
config.yaml              # Parámetros generales (paths, logging, scraping)
requirements.txt         # Dependencias del entorno
.env.sample              # Plantilla de variables de entorno
data/                    # (Carpetas vacías en repositorio; se llenan localmente)
	raw/
	interim/
	processed/
docs/                    # Documentación y reportes EDA
reports/visualizations/  # Salida de artefactos HTML (mapas/gráficos)
scripts/                 # Orquestación (ejecutar scraping masivo)
src/
	main.py                # Entrada Streamlit
	api/                   # FastAPI + plantillas HTML
	app/                   # Layout y componentes UI
	data_collection/       # Módulos de descarga (por período)
	eda/                   # Scripts EDA numerados
	utils/                 # Utilidades (logger, paths, helpers)
tests/                   # Pruebas smoke
```

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
### 1. Recolección / Descarga
Scripts específicos por semestre/año en `src/data_collection/` (ej: `codigo_2024_S1.py`). Para lanzar múltiples:
```bash
python scripts/ejecutar_todos_v2.py
```
Salidas crudas: `data/raw/` (o la ruta definida internamente). Ajustar rutas en los scripts si se requiere portabilidad (algunos ejemplos usan rutas absolutas Windows: reemplazarlas por relativas antes de producción).

### 2. Pipeline EDA / Limpieza
Los pasos están numerados (`01_...`, `02_...`). Convertir lógica validada en funciones reutilizables dentro de `src/eda/` o notebooks migrados. Resultado final esperado: `data/processed/denuncias_final.csv` (nombre puede variar según la convención final adoptada).

### 3. Aplicación Streamlit
```bash
streamlit run src/main.py
```
Accede en: http://localhost:8501

### 4. API FastAPI (servir visualizaciones HTML)
```bash
uvicorn src.api.main:app --reload
```
Accede en: http://127.0.0.1:8000

### 5. Pruebas
```bash
pytest -q
```

## 📊 Visualizaciones
Archivos HTML generados (mapas / gráficos) se almacenan en:
- `reports/visualizations/` (output general)
- `src/api/templates/` (los que la API expone)

Para integrarlos externamente: incrustar el HTML o servirlo via endpoint FastAPI.

## 🧱 Logger
Configurado en `src/utils/logger.py`, genera `logs/app.log`. Ajustar nivel vía variable de entorno o `config.yaml`.

## 🧪 Calidad / Buenas Prácticas
- Nombrado consistente de scripts por periodo (`codigo_<AÑO>_<S#>.py`).
- Separar lógica (funciones puras) de ejecución (bloque `if __name__ == "__main__"`).
- Evitar rutas absolutas (migrar a `Path` relativas + `config.yaml`).
- Añadir tests para módulos críticos (descarga, transformaciones clave).

## ❗ Problemas Frecuentes
| Situación | Causa | Solución |
|-----------|-------|----------|
| Mapas no cargan | Falta `MAPBOX_TOKEN` | Añadir token en `.env` |
| Descarga lenta / timeout | Límite servidor ArcGIS | Reducir ventana temporal o paginar por fecha |
| Error GeoJSON → fallback JSON | Endpoint no soporta geometría directa | Se maneja automáticamente en scripts `codigo_*.py` |
| Rutas Windows en Linux | Hardcode previo | Editar scripts y usar `os.path.join` / `pathlib.Path` |

## 🔮 Próximos Pasos (Roadmap sugerido)
- Centralizar parámetros de scraping (años/semestres) en un YAML.
- Incorporar caché incremental (solo nuevas denuncias).
- Tests de validación de esquema (pydantic / pandera).
- Dashboard de métricas (KPIs de delitos por turno / distrito).
- Automatización (Makefile / task runner / GitHub Actions).

## 🤝 Contribuir
1. Crear rama (`feature/nombre-feature`).
2. Añadir/actualizar tests si aplica.
3. Ejecutar `pytest -q` antes de hacer push.
4. Abrir PR con descripción clara del cambio.

## 👥 Autores
Equipo del curso - PC1. Uso académico / demostrativo.

---
Mantener este README alineado con el estado real del pipeline.

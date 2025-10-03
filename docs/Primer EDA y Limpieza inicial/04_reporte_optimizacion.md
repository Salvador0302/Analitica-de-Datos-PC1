# Paso 4: Optimización de Tipos de Datos (Numéricos)

En este paso, se optimizaron los tipos de datos de las columnas numéricas para reducir el uso de memoria y hacer el dataset más eficiente. La decisión de qué tipos usar se basó en el análisis de verificación del paso anterior.

## Acción Realizada

Se ejecutó el script `04_optimizar_tipos.py`.

*   **Archivo de Entrada**: `data_v2/denuncias_paso3.csv`
*   **Archivo de Salida**: `data_v2/denuncias_paso4.csv`

## Cambios Realizados

Se aplicaron las siguientes conversiones de tipo de dato (`astype`):

### Enteros (`int64` -> `int8` / `int16`)
*   `mes_hecho` -> `int8`
*   `dia_hecho` -> `int8`
*   `id_materia_hecho` -> `int8`
*   `id_dpto_hecho` -> `int8`
*   `solo_denuncia` -> `int8`
*   `estado` -> `int8`
*   `ano_hecho` -> `int16`
*   `id_tipo_hecho` -> `int16`

### Decimales (`float64` -> `float32`)
*   `lat` -> `float32`
*   `lon` -> `float32`
*   `lat_hecho` -> `float32`
*   `long_hecho` -> `float32`

El archivo `denuncias_paso4.csv` es el resultado de esta optimización y será el insumo para los siguientes pasos.

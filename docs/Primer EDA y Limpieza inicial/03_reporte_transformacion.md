# Paso 3: Transformación de Columnas

En este paso, el foco fue la estandarización y limpieza de las columnas de fecha y hora.

## Acción Realizada

Se ejecutó el script `03_transformar_columnas.py`.

*   **Archivo de Entrada**: `data_v2/denuncias_paso2.csv`
*   **Archivo de Salida**: `data_v2/denuncias_paso3.csv`

## Cambios Realizados

1.  **Conversión de Tipo de Dato**:
    *   La columna `fecha_hora_hecho` fue convertida de `object` (texto) a un tipo de dato `datetime64`. Las fechas que no pudieron ser interpretadas se convirtieron en `NaT` (Not a Time).

2.  **Columnas Eliminadas**:
    *   Se eliminaron las siguientes columnas por ser redundantes después de la estandarización de `fecha_hora_hecho`:
        *   `fecha_hecho`
        *   `hora_hecho`

El nuevo archivo `denuncias_paso3.csv` contiene ahora una columna de fecha y hora limpia y estandarizada, lista para análisis temporal.

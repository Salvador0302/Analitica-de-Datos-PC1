# Paso 7: Codificación y Binning

En este paso, se aplicaron varias técnicas de ingeniería de características para transformar columnas categóricas en formatos numéricos y para agrupar datos continuos, haciéndolos más útiles para el análisis y modelado.

## Acción Realizada

Se ejecutó el script `08_codificacion_y_binning.py`.

*   **Archivo de Entrada**: `data_v2/denuncias_paso5.csv`
*   **Archivo de Salida**: `data_v2/denuncias_paso7.csv`
*   **Diccionario de Datos**: `analysis/08_diccionario_codificacion.json`

## Transformaciones Realizadas

1.  **Limpieza de `estado_coord`**: Se unificaron los valores `'SIN COORDENADA XX'` y `'SIN COORDENADA YY'` en `'SIN COORDENADA'` para estandarizar la columna.

2.  **Codificación Ordinal de `turno_hecho`**: Se creó una nueva columna `turno_hecho_cod` con una representación numérica que conserva el orden natural de los turnos del día.
    *   `madrugada` -> `0`
    *   `mañana` -> `1`
    *   `tarde` -> `2`
    *   `noche` -> `3`

3.  **Binning de Hora a `periodo_dia`**: Se creó la columna `periodo_dia` agrupando la hora extraída de `fecha_hora_hecho` en cuatro categorías de texto.
    *   Horas 0-5 -> `'Madrugada'`
    *   Horas 6-11 -> `'Mañana'`
    *   Horas 12-17 -> `'Tarde'`
    *   Horas 18-23 -> `'Noche'`

4.  **Codificación Binaria de `estado_coord`**: Se creó la columna `tiene_coordenada` para representar de forma numérica (0 o 1) si el registro tiene o no coordenadas.
    *   `'CON COORDENADA'` -> `1`
    *   `'SIN COORDENADA'` -> `0`

## Diccionario de Datos

Todos los mapeos y transformaciones realizadas en este paso han sido documentados en el archivo `08_diccionario_codificacion.json` para garantizar la reproducibilidad y comprensión del dataset final.

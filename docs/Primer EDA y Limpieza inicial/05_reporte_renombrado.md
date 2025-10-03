# Paso 5: Renombrar y Estandarizar Columnas

En este paso, se estandarizaron los nombres de todas las columnas para asegurar un formato consistente y fácil de usar en análisis posteriores.

## Acción Realizada

Se ejecutó el script `05_renombrar_columnas.py`.

*   **Archivo de Entrada**: `data_v2/denuncias_paso4.csv`
*   **Archivo de Salida**: `data_v2/denuncias_paso5.csv`

## Cambios Realizados

Se aplicó una función de normalización a todos los nombres de columna. El proceso incluyó:
1.  Convertir todos los caracteres a minúsculas.
2.  Eliminar acentos y transliterar caracteres especiales (ej. `ñ` -> `n`).
3.  Reemplazar cualquier secuencia de caracteres no alfanuméricos por un único guion bajo (`_`).

El cambio más notable fue:
*   `año_hecho` -> `ano_hecho`

Otras columnas ya seguían un formato similar, por lo que sus nombres no cambiaron significativamente. El resultado es que todas las columnas ahora siguen el formato `snake_case`.

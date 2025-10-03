# Paso 2: Manejo de Valores Faltantes

En este paso, se realizó la primera fase de limpieza de datos, enfocada en eliminar columnas con un alto porcentaje de valores nulos (superior al 95%), basado en el diagnóstico del Paso 1.

## Acción Realizada

Se ejecutó el script `02_manejo_valores_faltantes.py` para procesar el archivo de datos completo.

*   **Archivo de Entrada**: `data_v2/denuncias_2020_2025.csv`
*   **Archivo de Salida**: `data_v2/denuncias_paso2.csv`

## Columnas Eliminadas

Las siguientes 9 columnas fueron eliminadas del conjunto de datos:

*   `tipologias_ia`
*   `cuadra_hecho`
*   `barrio`
*   `comisaria`
*   `departamento`
*   `provincia`
*   `distrito`
*   `indice_priorizacion`
*   `fecha_inaguracion`

El nuevo archivo `denuncias_paso2.csv` es el resultado de esta limpieza y será el insumo para los siguientes pasos.

# Paso 6: Eliminación de Duplicados

En este paso, se investigó la presencia de filas duplicadas en el conjunto de datos.

## Acción Realizada

Se ejecutó un script de verificación (`06_verificar_unicidad.py`) para analizar la unicidad de la columna `objectid`, que se había postulado como el identificador único de cada registro.

*   **Archivo Analizado**: `data_v2/denuncias_paso5.csv`
*   **Columna Verificada**: `objectid`

## Resultados

El script analizó el 100% del archivo y arrojó los siguientes resultados:

*   **Total de Filas Analizadas**: 7,425,530
*   **Valores Únicos de `objectid`**: 7,425,530

## Conclusión

Se ha confirmado que la columna `objectid` es un identificador único para todo el dataset. El número de filas es exactamente igual al número de valores únicos en esta columna.

**Por lo tanto, no existen filas duplicadas en el conjunto de datos y no es necesario realizar ninguna eliminación.**

El archivo para el siguiente paso seguirá siendo `denuncias_paso5.csv`.

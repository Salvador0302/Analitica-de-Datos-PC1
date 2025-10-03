# Paso 7 (Verificación): Análisis de Columnas Categóricas

Siguiendo el principio de "verificar antes de actuar", se realizó un análisis exhaustivo de las principales columnas categóricas para identificar el conjunto completo de sus valores únicos antes de proceder con la codificación.

## Acción Realizada

Se ejecutó el script `07_verificar_categoricas.py`.

*   **Archivo Analizado**: `data_v2/denuncias_paso5.csv`

## Resultados

El script generó un diccionario con los valores únicos para cada columna categórica analizada. Los resultados completos se encuentran en el archivo `analysis/07_diccionario_categoricas.json`.

A continuación, un resumen del número de valores únicos encontrados:

| Columna            | Valores Únicos |
|--------------------|----------------|
| departamento_hecho | 25             |
| provincia_hecho    | 196            |
| distrito_hecho     | 1732           |
| tipo_hecho         | 53             |
| materia_hecho      | 5              |
| turno_hecho        | 4              |
| es_delito_x        | 5              |
| macroregpol_hecho  | 23             |
| regionpol_hecho    | 29             |
| estado_coord       | 4              |

### Conclusión de la Verificación

*   Los valores en `turno_hecho` están limpios y listos para codificar.
*   La columna `estado_coord` contiene valores (`'SIN COORDENADA XX'`, `'SIN COORDENADA YY'`) que deben ser limpiados y unificados antes de la codificación.
*   El resto de las columnas tienen una cardinalidad (número de únicos) ahora conocida, lo que nos permite planificar mejor las estrategias de codificación o `get_dummies`.

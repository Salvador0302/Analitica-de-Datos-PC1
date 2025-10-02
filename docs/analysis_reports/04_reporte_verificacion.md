# Paso Intermedio: Verificación de Tipos de Datos

Antes de proceder con la optimización de tipos de datos, se realizó una verificación completa de todo el dataset para confirmar los rangos de valores y la cardinalidad de las columnas.

## Acción Realizada

Se ejecutó el script `04_verificar_tipos.py`, el cual leyó el 100% de las filas del archivo `data_v2/denuncias_paso3.csv`.

*   **Total de Filas Analizadas**: 7,425,530

## Resultados de la Verificación

### Rangos de Columnas Numéricas

| Columna        | Min Real      | Max Real     |
|----------------|---------------|--------------|
| mes_hecho      | 1             | 12           |
| dia_hecho      | 1             | 31           |
| id_tipo_hecho  | 101           | 714          |
| id_materia_hecho| 1             | 7            |
| ano_hecho      | 2020          | 2025         |
| id_dpto_hecho  | 1             | 25           |
| solo_denuncia  | 0             | 1            |
| estado         | 1             | 3            |
| lat            | -18.3485...   | -0.1196...   |
| lon            | -81.3244...   | -68.8183...  |
| lat_hecho      | -18.3485...   | -0.1196...   |
| long_hecho     | -81.3244...   | -68.8183...  |

### Conteo de Valores Únicos (Categóricas)

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

## Conclusión

La verificación confirma que es seguro y beneficioso optimizar los tipos de datos. Los rangos numéricos son pequeños y la cardinalidad de las columnas de texto es baja, lo que permitirá un ahorro significativo de memoria.

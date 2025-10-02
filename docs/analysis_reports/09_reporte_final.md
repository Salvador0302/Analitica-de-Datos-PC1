# Paso 8: Filtrado de Valores Atípicos

Este es el paso final del proceso de limpieza y preprocesamiento de datos. El objetivo fue eliminar registros que, por sus coordenadas geográficas, se consideran erróneos o atípicos.

## Acción Realizada

Se ejecutó el script `09_filtrar_atipicos.py`.

*   **Archivo de Entrada**: `data_v2/denuncias_paso7.csv`
*   **Archivo de Salida**: `data_v2/denuncias_final.csv`

## Cambios Realizados

Se aplicó un filtro geográfico basado en un "cajón" que encapsula las coordenadas de Perú.

*   **Límites de Latitud**: -18.4 a 0
*   **Límites de Longitud**: -81.4 a -68.6

Cualquier fila cuyas columnas `lat` y `lon` cayeran fuera de este rango fue eliminada del dataset. El script informó del número total de filas eliminadas durante este proceso.

## Conclusión del Proceso de Limpieza

Con este último paso, el proceso de limpieza de datos ha concluido. El archivo `denuncias_final.csv` contiene el conjunto de datos procesado y está listo para ser utilizado en análisis exploratorio, visualización o modelado de machine learning.

A lo largo de estos pasos, hemos:
1.  Diagnosticado el estado inicial de los datos.
2.  Eliminado columnas con exceso de valores nulos.
3.  Estandarizado y transformado las columnas de fecha.
4.  Optimizado los tipos de datos numéricos para eficiencia.
5.  Estandarizado los nombres de todas las columnas.
6.  Verificado y confirmado la ausencia de duplicados.
7.  Codificado y transformado variables categóricas.
8.  Filtrado valores atípicos geográficos.

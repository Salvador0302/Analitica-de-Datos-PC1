# Paso 1: Diagnóstico Inicial de Datos

Este documento resume el primer análisis exploratorio realizado sobre el conjunto de datos de denuncias.
El análisis se realizó sobre una muestra de las primeras **100,000 filas** para garantizar la eficiencia.

---

## 1. Información General y Tipos de Datos

*   **Total de filas en la muestra**: 100,000
*   **Uso de memoria en la muestra**: 194.03 MB

| Columna                   |   Valores No Nulos | Tipo de Dato   |
|:--------------------------|-------------------:|:---------------|
| fecha_hora_hecho          |             100000 | object         |
| mes_hecho                 |             100000 | int64          |
| dia_hecho                 |             100000 | int64          |
| departamento_hecho        |             100000 | object         |
| provincia_hecho           |             100000 | object         |
| distrito_hecho            |             100000 | object         |
| tipo_hecho                |             100000 | object         |
| id_tipo_hecho             |             100000 | int64          |
| materia_hecho             |             100000 | object         |
| id_materia_hecho          |             100000 | int64          |
| lat                       |             100000 | float64        |
| lon                       |             100000 | float64        |
| lat_hecho                 |             100000 | float64        |
| long_hecho                |             100000 | float64        |
| id_dgc                    |             100000 | int64          |
| ubigeo_cia_registro       |             100000 | int64          |
| id_comisaria_registro     |             100000 | int64          |
| comisaria_registro        |             100000 | object         |
| ubic_comisaria_registro   |             100000 | object         |
| ubigeo_cia_hecho          |             100000 | float64        |
| comisaria_hecho           |             100000 | object         |
| tipo_via_hecho            |             100000 | object         |
| cuadra_hecho              |               4594 | float64        |
| direccion_hecho           |             100000 | object         |
| turno_hecho               |             100000 | object         |
| ano_hecho                 |             100000 | int64          |
| ubigeo_hecho_delito       |             100000 | int64          |
| id_dpto_hecho             |             100000 | int64          |
| id_prov_hecho             |             100000 | int64          |
| id_dist_hecho             |             100000 | int64          |
| solo_denuncia             |             100000 | int64          |
| es_delito_x               |             100000 | object         |
| cod_uni_hecho             |             100000 | float64        |
| cod_cpnp_hecho            |             100000 | float64        |
| id_subtipo_hecho          |             100000 | int64          |
| subtipo_hecho             |             100000 | object         |
| id_modalidad_hecho        |             100000 | int64          |
| modalidad_hecho           |             100000 | object         |
| cod_macroregpol_hecho     |             100000 | float64        |
| macroregpol_hecho         |             100000 | object         |
| cod_regpol_hecho          |             100000 | object         |
| regionpol_hecho           |             100000 | object         |
| cod_divpol_divopus_hecho  |             100000 | object         |
| divpol_divopus_hecho      |             100000 | object         |
| fuente                    |             100000 | object         |
| tipologias_ia             |                  0 | float64        |
| estado                    |             100000 | int64          |
| estado_coord              |             100000 | object         |
| observacion               |             100000 | object         |
| objectid                  |             100000 | int64          |
| fecha_hora_registro_hecho |             100000 | int64          |
| barrio                    |               1173 | object         |
| comisaria                 |               1173 | object         |
| departamento              |               1173 | object         |
| provincia                 |               1173 | object         |
| distrito                  |               1173 | object         |
| indice_priorizacion       |               1173 | object         |
| fecha_inaguracion         |               1173 | float64        |
| fecha_hecho               |             100000 | object         |
| hora_hecho                |             100000 | object         |

---

## 2. Resumen de Valores Faltantes

| Columna             |   Valores Faltantes |   % Faltante |
|:--------------------|--------------------:|-------------:|
| tipologias_ia       |              100000 |      100     |
| provincia           |               98827 |       98.827 |
| barrio              |               98827 |       98.827 |
| comisaria           |               98827 |       98.827 |
| departamento        |               98827 |       98.827 |
| indice_priorizacion |               98827 |       98.827 |
| distrito            |               98827 |       98.827 |
| fecha_inaguracion   |               98827 |       98.827 |
| cuadra_hecho        |               95406 |       95.406 |

---

## 3. Estadísticas Descriptivas (Numéricas)

```
                              count          mean           std           min           25%           50%           75%           max
mes_hecho                  100000.0  3.715260e+00  1.731142e+00  1.000000e+00  2.000000e+00  4.000000e+00  5.000000e+00  6.000000e+00
dia_hecho                  100000.0  1.616486e+01  8.791374e+00  1.000000e+00  8.000000e+00  1.700000e+01  2.400000e+01  3.100000e+01
id_tipo_hecho              100000.0  5.080908e+02  1.916612e+02  1.010000e+02  6.020000e+02  6.020000e+02  6.020000e+02  6.020000e+02
id_materia_hecho           100000.0  5.051940e+00  1.934285e+00  1.000000e+00  6.000000e+00  6.000000e+00  6.000000e+00  6.000000e+00
lat                        100000.0 -1.187008e+01  3.324638e+00 -1.830722e+01 -1.353923e+01 -1.205116e+01 -9.626249e+00 -2.873111e+00
lon                        100000.0 -7.560827e+01  2.893122e+00 -8.130605e+01 -7.709591e+01 -7.690581e+01 -7.292575e+01 -6.894548e+01
lat_hecho                  100000.0 -1.187008e+01  3.324638e+00 -1.830722e+01 -1.353923e+01 -1.205116e+01 -9.626249e+00 -2.873111e+00
long_hecho                 100000.0 -7.560827e+01  2.893122e+00 -8.130605e+01 -7.709591e+01 -7.690581e+01 -7.292575e+01 -6.894548e+01
id_dgc                     100000.0  1.707378e+07  3.609497e+05  1.075825e+07  1.677340e+07  1.723130e+07  1.734397e+07  1.753198e+07
ubigeo_cia_registro        100000.0  1.206791e+05  5.976717e+04  1.010100e+04  6.010800e+04  1.305010e+05  1.501350e+05  2.503050e+05
id_comisaria_registro      100000.0  1.816127e+03  6.722751e+02  1.002000e+03  1.421000e+03  1.621000e+03  2.089000e+03  4.758000e+03
ubigeo_cia_hecho           100000.0  1.206918e+05  5.979485e+04  1.010100e+04  6.010800e+04  1.306010e+05  1.501350e+05  2.503050e+05
cuadra_hecho                 4594.0  1.927645e+01  7.972110e+01  0.000000e+00  2.000000e+00  4.000000e+00  9.000000e+00  9.650000e+02
ano_hecho                  100000.0  2.020000e+03  0.000000e+00  2.020000e+03  2.020000e+03  2.020000e+03  2.020000e+03  2.020000e+03
ubigeo_hecho_delito        100000.0  1.206791e+05  5.976717e+04  1.010100e+04  6.010800e+04  1.305010e+05  1.501350e+05  2.503050e+05
id_dpto_hecho              100000.0  1.204491e+01  5.982813e+00  1.000000e+00  6.000000e+00  1.300000e+01  1.500000e+01  2.500000e+01
id_prov_hecho              100000.0  1.206840e+03  5.979304e+02  1.010000e+02  6.010000e+02  1.306000e+03  1.501000e+03  2.503000e+03
id_dist_hecho              100000.0  1.206934e+05  5.979447e+04  1.010100e+04  6.010800e+04  1.306010e+05  1.501350e+05  2.503050e+05
solo_denuncia              100000.0  2.094500e-01  4.069181e-01  0.000000e+00  0.000000e+00  0.000000e+00  0.000000e+00  1.000000e+00
cod_uni_hecho              100000.0  2.198628e+05  2.085568e+03  2.160370e+05  2.185160e+05  2.198730e+05  2.216910e+05  2.265920e+05
cod_cpnp_hecho             100000.0  3.224168e+03  1.766205e+03  6.000000e+02  1.920000e+03  3.004000e+03  4.287000e+03  8.410000e+03
id_subtipo_hecho           100000.0  5.085661e+04  1.918835e+04  1.010100e+04  6.025500e+04  6.025800e+04  6.026100e+04  6.027000e+04
id_modalidad_hecho         100000.0  5.085668e+06  1.918834e+06  1.010101e+06  6.025599e+06  6.025802e+06  6.026101e+06  6.027001e+06
cod_macroregpol_hecho      100000.0  1.056237e+01  5.526720e+00  1.000000e+00  6.000000e+00  1.200000e+01  1.300000e+01  2.300000e+01
tipologias_ia                   0.0           NaN           NaN           NaN           NaN           NaN           NaN           NaN
estado                     100000.0  2.697670e+00  7.162204e-01  1.000000e+00  3.000000e+00  3.000000e+00  3.000000e+00  3.000000e+00
objectid                   100000.0  3.221317e+05  1.482296e+05  1.000000e+00  1.838838e+05  4.164095e+05  4.414472e+05  4.687750e+05
fecha_hora_registro_hecho  100000.0  1.586609e+12  4.631258e+09  1.515067e+12  1.582272e+12  1.588160e+12  1.590341e+12  1.593511e+12
fecha_inaguracion            1173.0  1.566046e+12  6.592467e+10  1.493942e+12  1.511482e+12  1.554941e+12  1.562198e+12  1.732234e+12
```

---

## 4. Estadísticas Descriptivas (Categóricas)

```
                           count unique                                                          top    freq
fecha_hora_hecho          100000  35324                                          2020-03-30 05:00:00     119
departamento_hecho        100000     25                                                         LIMA   29740
provincia_hecho           100000    193                                                         LIMA   26777
distrito_hecho            100000   1103                                            VILLA EL SALVADOR    2916
tipo_hecho                100000     26                                      INTERVENCION POLICIALES   78474
materia_hecho             100000      4                                   HECHOS DE INTERES POLICIAL   79112
comisaria_registro        100000   1184                           COMISARIA DE LA FAMILIA - AYACUCHO    3552
ubic_comisaria_registro   100000    968                                                 28  de julio    3552
comisaria_hecho           100000    975                                                CPNP AYACUCHO    3658
tipo_via_hecho            100000     16                                                        Otros   67453
direccion_hecho           100000  75267                            JURISDICCION DE LA CPNP JERUSALEN     156
turno_hecho               100000      4                                                       mañana   37956
es_delito_x               100000      5                                                        Otros   79219
subtipo_hecho             100000    104                                         CONTROL DE IDENTIDAD   43690
modalidad_hecho           100000    258  ESTADO DE EMERGENCIA - INCUMPLIMIENTO DEL D.S.-044-2020-PCM   43690
macroregpol_hecho         100000     23                                                         LIMA   29738
cod_regpol_hecho          100000     27                                                         13R1   29738
regionpol_hecho           100000     29                                                         LIMA   27229
cod_divpol_divopus_hecho  100000     58                                                        03R1A   13545
divpol_divopus_hecho      100000     58                                             DIVOPUS AREQUIPA   13545
fuente                    100000      1                                                         DGIS  100000
estado_coord              100000      2                                               SIN COORDENADA   84898
observacion               100000      6                        GEO FORZADA AL CENTROIDE DE COMISARIA   83961
barrio                      1173     78                                    LAYKAKOTA - RICARDO PALMA     248
comisaria                   1173     76                                           CIA SECTORIAL PUNO     248
departamento                1173     19                                                         LIMA     453
provincia                   1173     28                                                         LIMA     451
distrito                    1173     71                                                         PUNO     248
indice_priorizacion         1173     54                                                         1.15     368
fecha_hecho               100000    183                                                   07/05/2020    1360
hora_hecho                100000   1424                                                     05:00:00    6707
```

---

## 5. Distribución para Categorías Clave (Top 10)

### Distribución para 'departamento_hecho' (% sobre la muestra)
```
departamento_hecho
LIMA           29.740
AREQUIPA       13.545
LA LIBERTAD     8.082
JUNIN           5.819
AYACUCHO        4.691
TACNA           4.083
LAMBAYEQUE      3.550
CUSCO           3.250
ANCASH          2.960
ICA             2.861
```

### Distribución para 'tipo_hecho' (% sobre la muestra)
```
tipo_hecho
INTERVENCION POLICIALES                                        78.474
PATRIMONIO (DELITO)                                            11.531
SEGURIDAD PUBLICA (DELITO)                                      2.646
LEY DE VIOLENCIA CONTRA LA MUJER Y GRUPOS VULNERABLES           2.288
VIDA, EL CUERPO Y LA SALUD (DELITO)                             1.710
LIBERTAD (DELITO)                                               1.426
DENUNCIAS ESPECIALES                                            0.638
ADMINISTRACION PUBLICA (DELITO)                                 0.485
FALTAS                                                          0.420
LEY 30096 DELITOS INFORMATICOS, MODIFICADA POR LA LEY 30171     0.146
```

### Distribución para 'turno_hecho' (% sobre la muestra)
```
turno_hecho
mañana       37.956
madrugada    28.667
tarde        20.557
noche        12.820
```

### Distribución para 'ano_hecho' (% sobre la muestra)
```
ano_hecho
2020    100.0
```

### Distribución para 'mes_hecho' (% sobre la muestra)
```
mes_hecho
5    28.917
6    16.213
2    15.965
1    15.379
4    11.776
3    11.750
```


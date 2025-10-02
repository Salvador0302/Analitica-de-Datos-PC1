import os
import unicodedata
import requests
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

BASE_QUERY_URL = "https://seguridadciudadana.mininter.gob.pe/arcgis/rest/services/servicios_ogc/denuncias/MapServer/0/query"

# La cláusula WHERE ahora se construirá dinámicamente.
# WHERE = "(año_hecho >=2020)" # Ya no se usa

OUT_DIR = r"C:\Users\Tekim\Desktop\WebScrap\data"
OUT_CSV = os.path.join(OUT_DIR, "denuncias_LIMA_2020_completo.csv") # Cambiado para no sobreescribir

OUT_FIELDS = "*"
PAGE_SIZE = 1000  # Reducido para ser más amigable con la API
TIMEOUT = 60


def normalize_name(s: str) -> str:
    if not isinstance(s, str):
        return s
    s1 = ''.join(c for c in unicodedata.normalize('NFKD', s) if not unicodedata.combining(c))
    s1 = s1.replace('Ñ', 'N').replace('ñ', 'n')
    s1 = s1.strip().lower().replace(' ', '_')
    return s1


def json_to_gdf(esri_json):
    features = esri_json.get("features", [])
    if not features:
        return gpd.GeoDataFrame()
    wkid = esri_json.get("spatialReference", {}).get("wkid", 4326)
    xs, ys, attrs = [], [], []
    for f in features:
        g = f.get("geometry") or {}
        x, y = g.get("x"), g.get("y")
        xs.append(x)
        ys.append(y)
        attrs.append(f.get("attributes", {}))
    df = pd.DataFrame(attrs)
    geom = [Point(x, y) if (x is not None and y is not None) else None for x, y in zip(xs, ys)]
    gdf = gpd.GeoDataFrame(df, geometry=geom)
    gdf = gdf.set_crs(epsg=wkid or 4326, allow_override=True).to_crs(epsg=4326)
    return gdf


def fetch_page(session, where_clause, order_by="1", use_geojson_first=True):
    """Hace una única petición a la API, intentando con GeoJSON primero."""
    params = {
        "where": where_clause,
        "outFields": OUT_FIELDS,
        "returnGeometry": "true",
        "outSR": "4326",
        "f": "geojson",
        "orderByFields": order_by,
        "resultRecordCount": PAGE_SIZE
    }
    if use_geojson_first:
        try:
            r = session.get(BASE_QUERY_URL, params=params, timeout=TIMEOUT, verify=False)
            r.raise_for_status()
            txt = r.text.strip()
            if not txt.startswith("<") and len(txt) > 2:
                gdf = gpd.read_file(r.text).to_crs(epsg=4326)
                return gdf, len(gdf) >= PAGE_SIZE
        except Exception as e:
            print(f"Fallo al usar GeoJSON, reintentando con JSON. Error: {e}")
            # Pasa al método JSON si GeoJSON falla

    # Fallback a JSON
    params["f"] = "json"
    r = session.get(BASE_QUERY_URL, params=params, timeout=TIMEOUT, verify=False)
    r.raise_for_status()
    data = r.json()
    if "error" in data:
        raise RuntimeError(f"Error de la API: {data['error']}")
    
    gdf = json_to_gdf(data)
    exceeded = data.get("exceededTransferLimit", False)
    return gdf, exceeded or (len(gdf) >= PAGE_SIZE)


def fetch_all():
    """
    Descarga todos los registros desde 2020 hasta la fecha actual,
    iterando por fecha para superar el límite de registros del servidor.
    """
    session = requests.Session()
    all_pages = []
    
    start_date = pd.to_datetime("2020-01-01 00:00:00+00:00")
    last_timestamp_ms = int(start_date.timestamp() * 1000)

    print(f"Iniciando descarga desde: {start_date.strftime('%Y-%m-%d')}")

    while True:
        # La sintaxis correcta para fechas en ArcGIS es con timestamp 'YYYY-MM-DD HH:MI:SS'
        last_date_str = pd.to_datetime(last_timestamp_ms, unit='ms').strftime('%Y-%m-%d %H:%M:%S')
        where_clause = f"fecha_hora_hecho > timestamp '{last_date_str}'"
        print(f"Buscando registros con '{where_clause}'...")
        
        gdf, has_more = fetch_page(session, where_clause, order_by="fecha_hora_hecho")
        
        if gdf.empty:
            print("No se encontraron más registros. Descarga completa.")
            break
        
        all_pages.append(gdf)
        
        current_max_timestamp = gdf['fecha_hora_hecho'].max()
        
        if current_max_timestamp == last_timestamp_ms:
            print("No hay más registros nuevos (timestamp no avanza). Descarga completa.")
            break
            
        last_timestamp_ms = current_max_timestamp
        
        last_date_found = pd.to_datetime(last_timestamp_ms, unit='ms')
        print(f"Lote descargado. Última fecha: {last_date_found.strftime('%Y-%m-%d %H:%M:%S')}. ¿Más?: {has_more}")

        if not has_more:
            print("El servidor indica que no hay más páginas. Descarga completa.")
            break

    if not all_pages:
        return gpd.GeoDataFrame()

    gdf_all = pd.concat(all_pages, ignore_index=True).drop_duplicates(subset=['objectid'])
    if not isinstance(gdf_all, gpd.GeoDataFrame):
        gdf_all = gpd.GeoDataFrame(gdf_all)
    if gdf_all.crs is None:
        gdf_all = gdf_all.set_crs(epsg=4326, allow_override=True)
    else:
        gdf_all = gdf_all.to_crs(epsg=4326)

    # normaliza nombres
    gdf_all = gdf_all.rename(columns={c: normalize_name(c) for c in gdf_all.columns})

    # lat/lon desde geometría; si existen lat_hecho/long_hecho válidos, sobrescriben
    gdf_all["lat"] = gdf_all.geometry.y
    gdf_all["lon"] = gdf_all.geometry.x
    if "lat_hecho" in gdf_all.columns and "long_hecho" in gdf_all.columns:
        lat_num = pd.to_numeric(gdf_all["lat_hecho"], errors="coerce")
        lon_num = pd.to_numeric(gdf_all["long_hecho"], errors="coerce")
        mask = lat_num.notna() & lon_num.notna()
        gdf_all.loc[mask, "lat"] = lat_num[mask]
        gdf_all.loc[mask, "lon"] = lon_num[mask]

    return gdf_all


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    gdf = fetch_all()
    if gdf.empty:
        print("No se obtuvieron registros con el filtro dado.")
        return

    preferred = [
        "fecha_hecho", "hora_hecho", "fecha_hora_hecho",
        "anio_hecho", "mes_hecho", "dia_hecho",
        "departamento_hecho", "provincia_hecho", "distrito_hecho",
        "tipo_hecho", "id_tipo_hecho", "materia_hecho", "id_materia_hecho",
        "lat", "lon", "lat_hecho", "long_hecho"
    ]
    cols = [c for c in preferred if c in gdf.columns] + \
           [c for c in gdf.columns if c not in (preferred + ["geometry"])]

    df_out = pd.DataFrame(gdf[cols]).dropna(subset=["lat", "lon"])
    df_out = df_out[(df_out["lat"].between(-90, 90)) & (df_out["lon"].between(-180, 180))].copy()

    # Convertir y separar fecha y hora
    if 'fecha_hora_hecho' in df_out.columns:
        df_out['fecha_hora_hecho'] = pd.to_datetime(df_out['fecha_hora_hecho'], unit='ms', errors='coerce')

        # Crear solo fecha_hecho y hora_hecho
        df_out['fecha_hecho'] = df_out['fecha_hora_hecho'].dt.strftime('%d/%m/%Y')
        df_out['hora_hecho'] = df_out['fecha_hora_hecho'].dt.strftime('%H:%M:%S')

    df_out.to_csv(OUT_CSV, index=False, encoding="utf-8")
    print(f"Guardado: {OUT_CSV} Filas: {len(df_out)}")
    print(df_out.head(10).to_string(index=False))


if __name__ == "_main_":
    main()
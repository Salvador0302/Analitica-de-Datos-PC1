import os
import unicodedata
import requests
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

BASE_QUERY_URL = "https://seguridadciudadana.mininter.gob.pe/arcgis/rest/services/servicios_ogc/denuncias/MapServer/0/query"

# Filtros
WHERE = "(año_hecho = 2024 AND mes_hecho = 7 AND departamento_hecho = 'LIMA')"

OUT_DIR = r"C:\Users\Tekim\Desktop\WebScrap\data"
OUT_CSV = os.path.join(OUT_DIR, "denuncias_LIMA_2024_07.csv")

OUT_FIELDS = "*"
TIMEOUT = 60
BATCH_SIZE = 1000   # tamaño inicial del bloque de objectIds

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
        xs.append(x); ys.append(y)
        attrs.append(f.get("attributes", {}))
    df = pd.DataFrame(attrs)
    geom = [Point(x, y) if (x is not None and y is not None) else None for x, y in zip(xs, ys)]
    gdf = gpd.GeoDataFrame(df, geometry=geom)
    gdf = gdf.set_crs(epsg=wkid or 4326, allow_override=True).to_crs(epsg=4326)
    return gdf

def get_meta(session):
    # leer metadatos del layer (POST para ser consistentes)
    r = session.post(BASE_QUERY_URL.replace("/query", ""), data={"f": "json"}, timeout=TIMEOUT, verify=False)
    r.raise_for_status()
    meta = r.json()
    oid_field = meta.get("objectIdField", meta.get("objectIdFieldName", "OBJECTID"))
    return oid_field

def get_all_object_ids(session, oid_field):
    # pedir solo IDs (POST)
    data = {"where": WHERE, "returnIdsOnly": "true", "f": "json"}
    r = session.post(BASE_QUERY_URL, data=data, timeout=TIMEOUT, verify=False)
    r.raise_for_status()
    j = r.json()
    oids = j.get("objectIds") or j.get("objectIDs") or []
    return sorted(oids)

def _post_geojson(session, ids_str):
    data = {
        "objectIds": ids_str,
        "outFields": OUT_FIELDS,
        "returnGeometry": "true",
        "outSR": "4326",
        "f": "geojson"
    }
    r = session.post(BASE_QUERY_URL, data=data, timeout=TIMEOUT, verify=False)
    r.raise_for_status()
    txt = r.text.strip()
    if txt.startswith("<"):
        raise ValueError("Respuesta no-geojson")
    return gpd.read_file(r.text).to_crs(epsg=4326)

def _post_json(session, ids_str):
    data = {
        "objectIds": ids_str,
        "outFields": OUT_FIELDS,
        "returnGeometry": "true",
        "outSR": "4326",
        "f": "json"
    }
    r = session.post(BASE_QUERY_URL, data=data, timeout=TIMEOUT, verify=False)
    r.raise_for_status()
    return json_to_gdf(r.json())

def fetch_by_ids_chunk(session, ids_chunk):
    """Descarga un bloque de registros por objectIds usando POST."""
    ids_str = ",".join(map(str, ids_chunk))
    # 1) intentar GeoJSON
    try:
        return _post_geojson(session, ids_str)
    except Exception:
        # 2) caer a esriJSON
        return _post_json(session, ids_str)

def fetch_all():
    session = requests.Session()

    oid_field = get_meta(session)
    oids = get_all_object_ids(session, oid_field)
    total = len(oids)
    if not oids:
        print("No hay registros para el WHERE dado.")
        return gpd.GeoDataFrame()
    print(f"Total de registros a descargar: {total}")

    all_gdfs = []
    i = 0
    current_batch = BATCH_SIZE
    # bucle manual para poder reducir tamaño de bloque si aparece 414
    while i < total:
        end = min(i + current_batch, total)
        chunk = oids[i:end]
        try:
            gdf = fetch_by_ids_chunk(session, chunk)
            if not gdf.empty:
                all_gdfs.append(gdf)
            i = end
            pct = min(100, int(i * 100 / total))
            print(f"Descarga: {i} / {total}  ({pct}%)  [chunk={current_batch}]")
            # si todo bien varias veces, podemos intentar subir un poco el chunk (opcional)
            # current_batch = min(BATCH_SIZE, current_batch + 200)
        except requests.HTTPError as e:
            # si es 414, reducimos el chunk y reintentamos
            if e.response is not None and e.response.status_code == 414:
                if current_batch <= 50:
                    raise  # muy pequeño, abortar
                current_batch = max(50, current_batch // 2)
                print(f"414 URI Too Long → reduciendo chunk a {current_batch} y reintentando…")
            else:
                raise

    if not all_gdfs:
        return gpd.GeoDataFrame()

    gdf_all = pd.concat(all_gdfs, ignore_index=True)
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

    # asegurar CRS
    if isinstance(gdf_all, gpd.GeoDataFrame):
        if gdf_all.crs is None:
            gdf_all = gdf_all.set_crs(epsg=4326, allow_override=True)
        else:
            gdf_all = gdf_all.to_crs(epsg=4326)

    return gdf_all

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    gdf = fetch_all()
    if gdf.empty:
        print("No se obtuvieron registros con el filtro dado.")
        return

    preferred = [
        "fecha_hora_hecho","anio_hecho","mes_hecho","dia_hecho",
        "departamento_hecho","provincia_hecho","distrito_hecho",
        "tipo_hecho","id_tipo_hecho","materia_hecho","id_materia_hecho",
        "lat","lon","lat_hecho","long_hecho"
    ]
    cols = [c for c in preferred if c in gdf.columns] + \
           [c for c in gdf.columns if c not in (preferred + ["geometry"])]

    df_out = pd.DataFrame(gdf[cols]).dropna(subset=["lat","lon"])
    df_out = df_out[(df_out["lat"].between(-90,90)) & (df_out["lon"].between(-180,180))]

    df_out.to_csv(OUT_CSV, index=False, encoding="utf-8")
    print(f"Guardado: {OUT_CSV}  Filas: {len(df_out)}")
    print(df_out.head(10).to_string(index=False))

if __name__ == "__main__":
    main()

import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GEOJSON = ROOT / "data" / "geojson"
SOURCES = ROOT / "rml" / "sources"
OUT = ROOT / "data" / "csv" / "nearTo.csv"

NEAR_RADIUS_M = 2000
EARTH_RADIUS_M = 6371008.8

# amenity_type -> (geojson file, RML source csv, name column in the csv)
AMENITIES = {
    "park": ("dlr_mainparks.geojson", "dlr_mainparks.csv", "park_name"),
    "tennis": ("dlr_tennisclubs.geojson", "dlr_tennisclubs.csv", "Name"),
    "skatepark": ("dlr_skateparks.geojson", "dlr_skateparks.csv", "Name"),
    "leisurecentre": ("dlr_leisurecentres.geojson", "dlr_leisurecentres.csv", "name"),
    "publictoilet": ("dlr_publictoilets.geojson", "dlr_publictoilets.csv", "Name"),
    "wifiaccess": ("dlr_wifiaccess.geojson", "dlr_wifiaccess.csv", "Name"),
}


def norm(s):
    return " ".join(str(s).split()).casefold()


def haversine_m(lat1, lon1, lat2, lon2):
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = p2 - p1, math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * EARTH_RADIUS_M * math.asin(math.sqrt(a))


def ring_centroid(ring):
    """Shoelace centroid + signed area of a closed ring of (x, y)."""
    a = cx = cy = 0.0
    for (x0, y0), (x1, y1) in zip(ring, ring[1:]):
        cross = x0 * y1 - x1 * y0
        a += cross
        cx += (x0 + x1) * cross
        cy += (y0 + y1) * cross
    a /= 2
    return (cx / (6 * a), cy / (6 * a), a) if a else (ring[0][0], ring[0][1], 0.0)


def polygon_centroid(geometry):
    """Area-weighted centroid (lat, lon) of a Polygon or MultiPolygon."""
    polys = [geometry["coordinates"]] if geometry["type"] == "Polygon" else geometry["coordinates"]
    lon0, lat0 = polys[0][0][0][0], polys[0][0][0][1]
    kx = math.radians(1) * EARTH_RADIUS_M * math.cos(math.radians(lat0))
    ky = math.radians(1) * EARTH_RADIUS_M
    total = sx = sy = 0.0
    for poly in polys:
        for i, ring in enumerate(poly):  # ring 0 = exterior, rest = holes
            pts = [((c[0] - lon0) * kx, (c[1] - lat0) * ky) for c in ring]
            x, y, a = ring_centroid(pts)
            sign = 1 if i == 0 else -1
            w = sign * abs(a)
            total += w
            sx += w * x
            sy += w * y
    return lat0 + (sy / total) / ky, lon0 + (sx / total) / kx


def load_amenities():
    points = []  # (type, id, lat, lon)
    for atype, (gj, src, name_col) in AMENITIES.items():
        ids = {}
        with open(SOURCES / src, encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                ids[norm(row[name_col])] = row["OBJECTID"].strip()
        with open(GEOJSON / gj, encoding="utf-8") as f:
            features = json.load(f)["features"]
        matched = set()
        for feat in features:
            props = feat["properties"]
            name = norm(
                props.get("park_name")
                or props.get("Name")
                or props.get("name")
            )
            if name not in ids:
                raise SystemExit(f"{atype}: geojson feature '{name}' has no row in {src}")
            geom = feat["geometry"]
            if geom["type"] == "Point":
                lon, lat = geom["coordinates"][:2]
            else:
                lat, lon = polygon_centroid(geom)
            points.append((atype, ids[name], lat, lon))
            matched.add(name)
        missing = set(ids) - matched
        if missing:
            print(f"WARNING {atype}: no coordinates for {sorted(missing)}; skipped")
    return points


def load_counters():
    with open(SOURCES / "counters.csv", encoding="utf-8", newline="") as f:
        return [(r["OBJECTID"], float(r["Lat"]), float(r["Long"])) for r in csv.DictReader(f)]


def main():
    counters = load_counters()
    rows = []
    for atype, aid, alat, alon in load_amenities():
        for cid, clat, clon in counters:
            d = haversine_m(alat, alon, clat, clon)
            if d <= NEAR_RADIUS_M:
                rows.append((atype, int(aid), int(cid), round(d)))
    order = {t: i for i, t in enumerate(AMENITIES)}
    rows.sort(key=lambda r: (order[r[0]], r[1], r[3], r[2]))
    with open(OUT, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["amenity_type", "amenity_id", "counter_id", "distance_m"])
        w.writerows(rows)
    print(f"wrote {len(rows)} rows to {OUT}")


if __name__ == "__main__":
    main()

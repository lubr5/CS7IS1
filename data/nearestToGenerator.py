import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nearToGenerator import AMENITIES, ROOT, haversine_m, load_amenities, load_counters

OUT = ROOT / "data" / "csv" / "nearestTo.csv"

def main():
    counters = load_counters()
    rows = []
    for atype, aid, alat, alon in load_amenities():
        d, cid = min((haversine_m(alat, alon, clat, clon), int(cid)) for cid, clat, clon in counters)
        rows.append((atype, int(aid), cid, round(d)))
    order = {t: i for i, t in enumerate(AMENITIES)}
    rows.sort(key=lambda r: (order[r[0]], r[1]))
    with open(OUT, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["amenity_type", "amenity_id", "counter_id", "distance_m"])
        w.writerows(rows)
    print(f"wrote {len(rows)} rows to {OUT}")


if __name__ == "__main__":
    main()
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nearToGenerator import AMENITIES, ROOT, haversine_m, load_amenities

OUT = ROOT / "data" / "csv" / "invertedNearestTo.csv"
# All 16 counters
COUNTERS = ROOT / "data" / "csv" / "dlr_footfallCounterLocations.csv"


def load_all_counters():
    with open(COUNTERS, encoding="utf-8-sig", newline="") as f:
        return [(r["OBJECTID"], float(r["Lat"]), float(r["Long"])) for r in csv.DictReader(f)]


def main():
    amenities = load_amenities()
    order = {t: i for i, t in enumerate(AMENITIES)}
    rows = []
    for cid, clat, clon in load_all_counters():
        d, _, atype, aid = min(
            (haversine_m(alat, alon, clat, clon), order[atype], atype, int(aid))
            for atype, aid, alat, alon in amenities
        )
        rows.append((int(cid), atype, aid, round(d)))
    rows.sort(key=lambda r: r[0])
    with open(OUT, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["counter_id", "amenity_type", "amenity_id", "distance_m"])
        w.writerows(rows)
    print(f"wrote {len(rows)} rows to {OUT}")

if __name__ == "__main__":
    main()
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data" / "csv" / "nearestTo.csv"
OUT = ROOT / "data" / "csv" / "invertedNearestTo.csv"

def main():
    with open(SRC, encoding="utf-8", newline="") as f:
        # nearestTo.csv: amenity_type, amenity_id, counter_id, distance_m
        rows = [(int(r["counter_id"]), r["amenity_type"], int(r["amenity_id"]), int(r["distance_m"]))
                for r in csv.DictReader(f)]
    rows.sort()
    with open(OUT, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["counter_id", "amenity_type", "amenity_id", "distance_m"])
        w.writerows(rows)

if __name__ == "__main__":
    main()
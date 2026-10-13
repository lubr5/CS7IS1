"""
dlr_footfallCounterLocations.csv has 16 counters, but only 7 are in the
footfall count files RML cannot filterrows, so we select them here. We also have to:
  - convert Date_of_op from dd/mm/yyyy hh:mm to an ISO date (xsd:date)
  - record the column prefix used in the footfall files for each counter,
    so the observations mapping can link back to the counter.
]
"""
import csv
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "data" / "csv" / "dlr_footfallCounterLocations.csv"
OUT = ROOT / "rml" / "sources" / "counters.csv"

# OBJECTID in the locations file -> column prefix in the footfall files
COUNTERS = {
    "1": "glenageary",
    "4": "rock_road_park",
    "8": "dun_laoghaire_seapoint_beach",
    "12": "dun_laoghaire_peoples_park",
    "13": "dun_laoghaire_york_road",
    "15": "wyattville_road_park_gates",
    "16": "wyattville_road_steps",
}

FIELDS = ["OBJECTID", "SITES", "Type", "Info", "Lat", "Long", "Date_of_op", "column_prefix"]


def main():
    with open(SRC, encoding="utf-8-sig", newline="") as f:
        rows = {r["OBJECTID"]: r for r in csv.DictReader(f)}

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for oid, prefix in COUNTERS.items():
            r = rows[oid]
            w.writerow({
                "OBJECTID": oid,
                "SITES": r["SITES"].strip(),
                "Type": r["Type"].strip(),
                "Info": r["Info"].strip(),
                "Lat": r["Lat"].strip(),
                "Long": r["Long"].strip(),
                "Date_of_op": datetime.strptime(r["Date_of_op"].strip(), "%d/%m/%Y %H:%M").date().isoformat(),
                "column_prefix": prefix,
            })
    print(f"wrote {len(COUNTERS)} counters to {OUT}")


if __name__ == "__main__":
    main()

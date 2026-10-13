"""
change footfall count from one column group per counter to one row pre counter, hour
Rows where a counter has no data for that hour (all three values blank) are
skipped, so counters with no readings produce no observations.
much nicer to map i hope its okay
"""
import csv
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "data" / "csv" / "dlr_footfallcount.csv"
COUNTERS = ROOT / "rml" / "sources" / "counters.csv"
OUT = ROOT / "rml" / "sources" / "observations.csv"

FIELDS = ["obs_id", "counter_id", "timestamp", "total", "in_count", "out_count"]


def main():
    # column prefix in the footfall file -> counter OBJECTID (from make_counters.py)
    with open(COUNTERS, encoding="utf-8", newline="") as f:
        counters = {r["column_prefix"]: r["OBJECTID"] for r in csv.DictReader(f)}

    n = 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(SRC, encoding="utf-8-sig", newline="") as fin, \
         open(OUT, "w", encoding="utf-8", newline="") as fout:
        w = csv.DictWriter(fout, fieldnames=FIELDS)
        w.writeheader()
        for row in csv.DictReader(fin):
            t = datetime.strptime(row["Time"].strip(), "%d/%m/%Y %H:%M")
            for prefix, cid in counters.items():
                vals = {k: row[f"{prefix}_{k}"].strip() for k in ("total", "in", "out")}
                if not any(vals.values()):
                    continue
                w.writerow({
                    "obs_id": f"{cid}-{t:%Y%m%d%H}",
                    "counter_id": cid,
                    "timestamp": t.isoformat(),
                    "total": vals["total"],
                    "in_count": vals["in"],
                    "out_count": vals["out"],
                })
                n += 1
    print(f"wrote {n} observations to {OUT}")


if __name__ == "__main__":
    main()

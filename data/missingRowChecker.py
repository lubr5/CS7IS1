import csv
from datetime import datetime, timedelta

# Change this to the directory of your files.
files = [
    "/Users/ollieeasterbrook/Desktop/github projects/CS7IS1/data/csv/historicalFootfall_pre2026/footfall2021.csv",
    "/Users/ollieeasterbrook/Desktop/github projects/CS7IS1/data/csv/historicalFootfall_pre2026/footfall2022.csv",
    "/Users/ollieeasterbrook/Desktop/github projects/CS7IS1/data/csv/historicalFootfall_pre2026/footfall2023.csv",
    "/Users/ollieeasterbrook/Desktop/github projects/CS7IS1/data/csv/historicalFootfall_pre2026/footfall2024.csv",
    "/Users/ollieeasterbrook/Desktop/github projects/CS7IS1/data/csv/historicalFootfall_pre2026/footfall2025.csv",
    "/Users/ollieeasterbrook/Desktop/github projects/CS7IS1/data/csv/dlr_footfallcount.csv",
]


for file in files:
    with open(file, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)

        times = [
            datetime.strptime(row["Time"].strip(), "%d/%m/%Y %H:%M")
            for row in reader
            if row["Time"].strip()
        ]

        times.sort()

        missing = []
        if times:
            expected = times[0]

            for actual in times:
                while expected < actual:
                    missing.append(expected)
                    expected += timedelta(hours=1)

                expected = actual + timedelta(hours=1)

        print(f"\nProcessing: {file}")
        print(f"Missing rows: {len(missing)}")

        for timestamp in missing:
            print(timestamp.strftime("%d/%m/%Y %H:%M"))

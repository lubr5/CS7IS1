import csv
from pathlib import Path

FINAL_HEADERS = [
    "Time",
    "dun_laoghaire_peoples_park_total",
    "dun_laoghaire_peoples_park_in",
    "dun_laoghaire_peoples_park_out",
    "dun_laoghaire_seapoint_beach_total",
    "dun_laoghaire_seapoint_beach_in",
    "dun_laoghaire_seapoint_beach_out",
    "dun_laoghaire_york_road_total",
    "dun_laoghaire_york_road_in",
    "dun_laoghaire_york_road_out",
    "glenageary_total",
    "glenageary_in",
    "glenageary_out",
    "n11_totem_inbound_total",
    "n11_totem_inbound_in",
    "n11_totem_inbound_out",
    "rock_road_park_total",
    "rock_road_park_in",
    "rock_road_park_out",
    "wyattville_road_bicycles_towards_n11_total",
    "wyattville_road_bicycles_towards_n11_in",
    "wyattville_road_bicycles_towards_n11_out",
    "wyattville_road_park_gates_total",
    "wyattville_road_park_gates_in",
    "wyattville_road_park_gates_out",
    "wyattville_road_steps_total",
    "wyattville_road_steps_in",
    "wyattville_road_steps_out",
]


def standardise_file(input_file, output_file):
    with open(input_file, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)

        existing_headers = reader.fieldnames

        print(f"\nProcessing: {input_file}")
        print(f"Headers: {existing_headers}")

        rows = list(reader)

        print(f"Number of rows: {len(rows)}")

        if rows:
            print(f"First Time: {rows[0]['Time']}")
            print(f"Last Time:  {rows[-1]['Time']}")

        # Check for unexpected headers
        unexpected = [
            h for h in existing_headers
            if h not in FINAL_HEADERS
        ]

        if unexpected:
            raise ValueError(f"Unexpected headers in {input_file}: {unexpected}")

        with open(output_file, "w", encoding="utf-8", newline="") as out:
            writer = csv.DictWriter(out, fieldnames=FINAL_HEADERS)

            writer.writeheader()

            for row in rows:
                new_row = {header: "" for header in FINAL_HEADERS}

                for header in existing_headers:
                    new_row[header] = row[header]

                writer.writerow(new_row)

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
    input_file = Path(file)
    output_file = input_file.with_name(input_file.stem + "_standardised.csv") # Manually rename once checked.
    standardise_file(input_file, output_file)

    print(f"Created: {output_file}")
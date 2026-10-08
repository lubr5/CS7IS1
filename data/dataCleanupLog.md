# Data Cleanup Log

**leisurecentres.csv:**

* Removed trailing spaces
* Normalised phone numbers

**tennisclubs.csv:**

* Removed trailing spaces
* Removed leading spaces
* Normalised phone numbers
* Fixed inconsistent OBJECTID so it now reads 1-15 instead of skipping numbers.
* *There is missing data that must be handled correctly in the query/KG setup e.g. missing coordinates, missing phone numbers and emails*

**mainparks.csv:**

* Removed leading spaces
* Fixed truncated header names e.g. "previous\_n --> previous\_name"
* Fixed error where Deerkpark was given the same address as People's Park (People's Park confirmed as correct)
* *Lots of missing data*
* *No coordinates, only polygon shapes*
* *Coordinates likely available in the equivalent geojson file*

**skateparks.csv:**

* Fixed inconsistency in address
* Removed pricing information from the "Info" column
* *A phone number is missing*

**footfallcount.csv:**

* Formatted as datetime instead of string

**footfall2021-25.csv:**

* Produced consistent header naming, fixising below issues.
* *2021 adds "Rock Road Park - New Counter" halfway through the year.*
* *2023 adds new header "Wyattville Rd - Bicycles Towards N11."*
* *2024 renames "Rock Road Park - New Counter" to Rock Road Park - "Ped's & Cyclists". Cleaned.*
* *2024 marks "Wyatville Road at Steps" as "Decomissioned/Historical". Cleaned to remove suffix.*
* *2026 adds new header "N11 Totem Inbound".*
* *2026 uses Pietons instead of Peds. Normalised.*
* TODO: ADD CORRECT NUMBER OF COMMAS TO DATASET IN CORRECT POSITION.
* *Lots of missing data.*



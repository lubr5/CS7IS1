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

*footfallYEAR.csv*

* Formatted as datetime instead of string.
* *Lots of missing data.*
* TODO?: *Missing rows. Can be seen for each file by running missingRowChecker.py.*


**footfall2021.csv:**

* Added normalised header naming based off of dlr_footfallcount. Also fixes below issues.
* *2021 adds "Rock Road Park - New Counter" halfway through the year.*

**footfall2022.csv:**

* Added normalised header naming based off of dlr_footfallcount.

**footfall2023.csv:**

* Added normalised header naming based off of dlr_footfallcount. Also fixes below issues.
* *2023 adds new header "Wyattville Rd - Bicycles Towards N11."*

**footfall2024.csv:**
* Added normalised header naming based off of dlr_footfallcount. Also fixes below issues.
* *2024 renames "Rock Road Park - New Counter" to Rock Road Park - "Ped's & Cyclists".*
* *2024 marks "Wyatville Road at Steps" as "Decomissioned/Historical".*


**footfall2025.csv:**
* Added normalised header naming based off of dlr_footfallcount. Also fixes below issues.

**dlr_footfallcount.csv:**
* Added normalised header naming based off of dlr_footfallcount. Also fixes below issues.
* *2026 adds new header "N11 Totem Inbound".*
* *2026 uses Pietons instead of Peds.*

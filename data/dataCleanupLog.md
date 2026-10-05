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

* TODO

**footfallcount.csv:**

* TODO


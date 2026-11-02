# CS7IS1 Group Project
## Lucia Brown, Oliver Easterbrook, Dylan Martin, Scott McNally, Finn Sprague

Design Doc Link: https://docs.google.com/document/d/1unlc_5MTcr2ldhm9-gVFyPqsqi90dCOrYPh6GVP0GxI/edit?tab=t.0 

### 1. Data Cleanup
✔️ - LUCIA & OLLIE

### 2. Implement ontology that defines KG schema
✔️  - LUCIA & OLLIE

### 3. Create at least 30 instance triples w/ RML mapping
✔️  - SCOTT & OLLIE

### 4. Create at least 3 instance validations w/ SHACL
✔️ - LUCIA 
shacl/validations.ttl <br>

_Validation 1: Validates that all the classes are correctly structured_ <br>
_Validation 2: Validates that instances of FootfallObservations have exactly one recordedBy property, and that property is an instance of FootfallCounter. Validates that instances of FootfallObservations have exactly one observedAt property and that property is a datetime value_ <br>
_Validation 3: Validates that every amenity has only one FootfallCounter considered as its nearestTo counter (real error in ontology!)_<br>

Validation 2 caught a **real** issue in the ontology on 2 Nov 2026 - see terminal SHACL running instructions <br>

#### SHACL Running Instructions (Linux Terminal & python3):
**Create concatenated file of the data**:<br>
`cat rml/output/{areas,amenity_areas,parks,sports,infrastructure,counters,observations,nearestTo,nearTo}.ttl > /tmp/all_data.ttl`<br>

**Get a full SHACL report**:<br>
`pyshacl -s shacl/validations.ttl -e ontology/dlr.ttl -df turtle /tmp/all_data.ttl`<br>

<img width="1847" height="535" alt="image" src="https://github.com/user-attachments/assets/3feb7e86-a237-405c-b0cc-463363a7dc30" />

**Simplified view (one line per violation)**:<br>
`pyshacl -s shacl/validations.ttl -e ontology/dlr.ttl -df turtle /tmp/all_data.ttl | awk '/^Constraint Violation/ {c=$4; sub(/Component.*/,"",c)} /Focus Node:/ {f=$3} /Value Node:/ {v=$3} /Message:/ {printf "%-18s %-30s %s\n", c, f, (v==""?"-":v); v=""}' | sed 's#<http://example.org/dlr/id/##g; s#>##g' | sort`
<img width="501" height="356" alt="image" src="https://github.com/user-attachments/assets/40a29ddf-d857-4b7c-81db-ee3b98014372" />


### 5. Create at least 7 queries on the data w/ SPARQL
IN PROG - FINN & DYLAN <br>
_Query 1: sparql/footfallAtEachPark.rq - The entire footfall at each park, based on the nearest footfall counter_
<img width="1528" height="519" alt="image" src="https://github.com/user-attachments/assets/d31d5b97-c9d2-4ce7-9d63-fb3749e2c85a" /> <br>
_Query 2: sparql/X.rq - [descriptivetext]_ <br>
_Query 3: sparql/X.rq - [descriptivetext]_ <br>
_Query 4: sparql/X.rq - [descriptive text]_ <br>
_Query 5: sparql/X.rq - [descriptive text]_ <br>
_Query 6: sparql/X.rq - [descriptive text]_ <br>
_Query 7: sparql/X.rq - descriptive text]_ <br>

### 6. PDF report of work
TODO

### 7. Everything Visualised on GraphDB
PARTIALLY DONE - LUCIA

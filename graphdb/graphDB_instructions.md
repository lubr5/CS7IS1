# Loading KG into GraphDB

This gets the whole project (ontology, instance data, GeoSPARQL geometries) into a local GraphDB so you can run the SPARQL queries and visualise the graph.<br>

You do **not** need to re-run RML or any Python script: the generated Turtle in `rml/output/` is already committed.

## 1. Create the repository

**Setup → Repositories → Create new repository → GraphDB Repository**

| Setting | Value |
|---|---|
| Repository ID | `GROUPB` |
| Ruleset | RDFS-Plus (Optimized) |

Tick **Enable SHACL Validation** before clicking **Create**<br>

Click **Create**, then pick `GROUPB` as the active repository (top-right dropdown).<br>

Enable GeoSPARQL by running this in the **SPARQL** tab:

```sparql
PREFIX : <http://www.ontotext.com/plugins/geosparql#>
INSERT DATA { _:s :enabled "true" . }
```

## 2. Import the data

**Import → Upload RDF files**, choose `graphdb/all_data.ttl`, import into the **default graph**.
**Import → Upload RDF files**, choose `shacl/validations.ttl`, import into the **named graph**: `http://rdf4j.org/schema/rdf4j#SHACLShapeGraph`

**Do not import:**
- `rml/output/exampleSchemaParks.ttl` 
- `data/geojson/*`

## 3. Check the import

In **SPARQL**:

```sparql
SELECT (COUNT(*) AS ?n) WHERE { ?s ?p ?o }
```

```sparql
PREFIX dlr: <http://example.org/dlr/ontology#>
SELECT ?s WHERE { ?s a dlr:Park } LIMIT 10
```

You should see a non-zero triple count and a list of parks.

## 4. Run the queries

Paste the contents of each file from `sparql/` into the **SPARQL** tab (and save them under **Saved queries**)

## 5. Visualise

- **Explore → Visual graph**: search for a park, counter or area IRI
- **Explore → Class hierarchy / Class relationships**: shows the ontology structure

## SHACL
Validation is already done with pySHACL (see README). The SHACL described in Step 2 just enforces the rules within GraphDB<br>
It does NOT give a validation report


# GeoJSON -> GeoSPARQL geometry
import csv
import json

from shapely import to_wkt
from shapely.geometry import shape

ID_BASE = "http://example.org/dlr/id"

PATHS = {
    "dlr_mainparks": "park",
    "dlr_tennisclubs": "tennis",
    "dlr_skateparks": "skatepark",
    "dlr_leisurecentres": "leisurecentre",
    "dlr_publictoilets": "publictoilet",
    "dlr_wifiaccess": "wifiaccess",
}



def geojson_to_geometry(file_name):
    
    with open(f"data/geojson/{file_name}.geojson") as file:
        features = json.load(file)["features"]
        
    geometries = []
    for feature in features:
        object_id = feature["properties"]["OBJECTID"]
        
        # each shape as parsable text
        wkt = to_wkt(shape(feature["geometry"]), output_dimension=2)
        
        geometries.append((object_id, wkt))

    return geometries



def read_counter_geometries():
    # geojson Counters have no id so use csv
    with open("rml/sources/counters.csv") as file:
        rows = list(csv.DictReader(file))

    geometries = []
    for row in rows:
        # WKT is long/lat 
        geometries.append((row["OBJECTID"], f"POINT({row['Long']} {row['Lat']})"))

    return geometries



def feature_triples(feature_iri, wkt):
    # Feature -> geometry -> WKT string
    geometry_iri = f"{feature_iri}/geom"

    return f"<{feature_iri}> a geo:Feature; geo:hasGeometry <{geometry_iri}>. <{geometry_iri}> a geo:Geometry; geo:asWKT '{wkt}'^^geo:wktLiteral .\n"



def main():
    output_content = "@prefix geo: <http://www.opengis.net/ont/geosparql#> .\n\n"

    datasets = {}
    for file in PATHS.keys():
        iri_path = PATHS[file]

        # the data doesnt have geosparql format
        # need to convert geojson to geometry node
        datasets[iri_path] = geojson_to_geometry(file)

    datasets["counter"] = read_counter_geometries()

    for iri_path, geometries in datasets.items():
        for object_id, wkt in geometries:
            feature_iri = f"{ID_BASE}/{iri_path}/{object_id}"
            output_content += feature_triples(feature_iri=feature_iri, wkt=wkt)

        # print(f"{iri_path}: {len(geometries)} features")

    with open("rml/output/geometry.ttl", "w") as output:
        output.write(output_content)



if __name__ == "__main__":
    main()

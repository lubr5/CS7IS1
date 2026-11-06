"""Validate the knowledge graph against all SHACL shapes in shacl/.

One-time setup:
    pip install pyshacl

Usage (from the repo root):
    python shacl/run_shacl.py                 # validate the real RML output
    python shacl/run_shacl.py shacl/test_invalid.ttl   # validate another data file
    python shacl/run_shacl.py --all           # also list every warning

It prints one line per problem, grouped by shape, and saves the full report
to shacl/report.txt (useful for the screenshot the spec asks for).
"""
import sys
from collections import Counter
from pathlib import Path

from pyshacl import validate
from rdflib import Graph, Namespace
from rdflib.namespace import RDF

ROOT = Path(__file__).resolve().parents[1]
SH = Namespace("http://www.w3.org/ns/shacl#")

DATA_FILES = [ROOT / "rml" / "output" / f"{n}.ttl" for n in (
    "areas", "amenity_areas", "parks", "sports", "infrastructure",
    "counters", "observations", "nearestTo", "nearTo",
)]
SHAPE_FILES = sorted((ROOT / "shacl").glob("*validations.ttl"))
ONTOLOGY = ROOT / "ontology" / "dlr.ttl"


def short(node):
    s = str(node)
    for prefix in ("http://example.org/dlr/id/", "http://example.org/dlr/ontology#",
                   "http://example.org/dlr/shapes#", "http://www.w3.org/ns/shacl#"):
        s = s.replace(prefix, "")
    return s


def main():
    data_files = [Path(p) for p in sys.argv[1:] if not p.startswith("--")] or DATA_FILES

    data = Graph()
    for f in data_files:
        data.parse(f, format="turtle")
    shapes = Graph()
    for f in SHAPE_FILES:
        shapes.parse(f, format="turtle")
    ontology = Graph().parse(ONTOLOGY, format="turtle")

    # ont_graph: mixes the ontology in so sh:targetClass dlr:Amenity also
    # matches Parks, SportsFacilities and Infrastructure (via rdfs:subClassOf).
    # inference="none": we check the data as RML produced it, without
    # letting a reasoner invent rdf:type triples that would hide mistakes.
    conforms, report_graph, report_text = validate(
        data, shacl_graph=shapes, ont_graph=ontology,
        inference="none", advanced=True, allow_warnings=True,
    )

    (ROOT / "shacl" / "report.txt").write_text(report_text, encoding="utf-8")

    rows = []
    for r in report_graph.subjects(RDF.type, SH.ValidationResult):
        shape = report_graph.value(r, SH.sourceShape)
        # Property shapes are blank nodes; name them after their parent node shape.
        parent = shapes.value(None, SH.property, shape) or shape
        rows.append((
            short(report_graph.value(r, SH.resultSeverity)),
            short(parent),
            short(report_graph.value(r, SH.focusNode)),
            short(report_graph.value(r, SH.value) or "-"),
            str(report_graph.value(r, SH.resultMessage)),
        ))

    print(f"Data: {len(data)} triples from {len(data_files)} file(s)")
    print(f"Shapes: {', '.join(f.name for f in SHAPE_FILES)}")
    print(f"Conforms: {conforms}\n")
    for sev, shape, focus, value, msg in sorted(rows):
        if sev == "Warning" and "--all" not in sys.argv:
            continue  # warnings are only counted below; pass --all to list them
        print(f"{sev:<9} {shape:<26} {focus:<26} {value:<22} {msg}")
    print("\nSummary:")
    for (sev, shape), n in sorted(Counter((r[0], r[1]) for r in rows).items()):
        print(f"  {n:>4}  {sev:<9} {shape}")
    print(f"\nFull report saved to {ROOT / 'shacl' / 'report.txt'}")


if __name__ == "__main__":
    main()

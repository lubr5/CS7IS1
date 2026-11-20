#!/usr/bin/env python3
"""
ttlviz.py - validate a Turtle file and visualise it as a graph.

Usage:
    python ttlviz.py mygraph.ttl
    python ttlviz.py mygraph.ttl --no-open      # don't open the browser

Install:
    pip install rdflib pyvis

Outputs (same directory as the input file):
    <name>.html   interactive graph (open in any browser)
"""
import argparse
import sys
import webbrowser
from pathlib import Path

try:
    from rdflib import Graph, Literal, URIRef, BNode, RDF, RDFS, OWL
except ImportError:
    sys.exit("rdflib is missing. Run: pip install rdflib pyvis")

# built in vocabularies
BUILTIN_PREFIXES = (
    str(RDF), str(RDFS),
    "http://www.w3.org/2001/XMLSchema#",
    "http://www.w3.org/2002/07/owl#",
)


def load(path: Path) -> Graph:
    g = Graph()
    try:
        g.parse(str(path), format="turtle")
    except Exception as e:  # rdflib raises several parser exception types
        print(f"\nINVALID TURTLE in {path.name}:\n  {e}\n")
        sys.exit(1)
    return g


def short(g: Graph, term) -> str:
    """Prefixed name for URIs, readable text for literals/blank nodes."""
    if isinstance(term, URIRef):
        try:
            prefix, _, local = g.namespace_manager.compute_qname(term, generate=False)
            return f"{prefix}:{local}" if prefix else local
        except Exception:
            s = str(term)
            return s.rsplit("#", 1)[-1].rsplit("/", 1)[-1] or s
    if isinstance(term, Literal):
        text = str(term)
        if term.language:
            return f'"{text}"@{term.language}'
        if term.datatype:
            dt = short(g, term.datatype)
            return f'"{text}"^^{dt}'
        return f'"{text}"'
    return f"_:{term}"


CARD_LABELS = {
    OWL.cardinality: "exactly {n}",
    OWL.minCardinality: "min {n}",
    OWL.maxCardinality: "max {n}",
}


def split_restrictions(g: Graph):
    """Collapse owl:Restriction blank nodes into plain class -> property edges.

    Returns (plain_triples, restriction_edges). restriction_edges is a list of
    (class, property, label); plain_triples excludes every triple that belongs
    to a restriction node or points at one.
    """
    restrictions = set(g.subjects(RDF.type, OWL.Restriction))
    edges = []
    for cls, _, r in g.triples((None, RDFS.subClassOf, None)):
        if r not in restrictions:
            continue
        prop = g.value(r, OWL.onProperty)
        if prop is None:
            continue
        for pred, fmt in CARD_LABELS.items():
            n = g.value(r, pred)
            if n is not None:
                edges.append((cls, prop, fmt.format(n=n)))
    plain = [(s, p, o) for s, p, o in g
             if s not in restrictions and o not in restrictions]
    return plain, edges


def report(g: Graph) -> None:
    print(f"\nParsed OK: {len(g)} triples")

    subjects = set(g.subjects())
    nodes = {t for s, _, o in g for t in (s, o) if not isinstance(t, Literal)}
    print(f"Distinct subjects: {len(subjects)}   Non-literal nodes: {len(nodes)}")

    classes = set(g.subjects(RDF.type, RDFS.Class))
    props = set(g.subjects(RDF.type, RDF.Property))
    print(f"Declared classes: {len(classes)}   Declared properties: {len(props)}")

    # Light schema checks, mainly useful for the RDFS task
    warnings = []

    used_preds = {p for _, p, _ in g if not str(p).startswith(BUILTIN_PREFIXES)}
    for p in sorted(used_preds, key=str):
        if p not in props:
            warnings.append(f"predicate {short(g, p)} is used but not declared as rdf:Property")
        else:
            if (p, RDFS.domain, None) not in g:
                warnings.append(f"property {short(g, p)} has no rdfs:domain")
            if (p, RDFS.range, None) not in g:
                warnings.append(f"property {short(g, p)} has no rdfs:range")

    used_types = {o for _, _, o in g.triples((None, RDF.type, None))
                  if isinstance(o, URIRef) and not str(o).startswith(BUILTIN_PREFIXES)}
    for c in sorted(used_types, key=str):
        if c not in classes:
            warnings.append(f"class {short(g, c)} is used as a type but not declared as rdfs:Class")

    untyped = [s for s in subjects
               if isinstance(s, URIRef)
               and (s, RDF.type, None) not in g
               and s not in classes and s not in props]
    for s in sorted(untyped, key=str):
        warnings.append(f"subject {short(g, s)} has no rdf:type")

    if warnings:
        print("\nWarnings (not errors; expected if you are still on the plain RDF task):")
        for w in warnings:
            print(f"  - {w}")
    else:
        print("\nNo schema warnings.")


def write_html(g: Graph, out: Path) -> None:
    try:
        from pyvis.network import Network
    except ImportError:
        print("pyvis is missing, skipping HTML graph. Run: pip install pyvis")
        return

    net = Network(height="900px", width="100%", directed=True,
                  bgcolor="#ffffff", font_color="#222222", cdn_resources="in_line")
    net.set_options("""
    {
      "physics": {"solver": "forceAtlas2Based",
                  "forceAtlas2Based": {"springLength": 160, "avoidOverlap": 0.6}},
      "edges": {"font": {"size": 12, "align": "middle"}, "smooth": {"type": "dynamic"}}
    }
    """)

    added = set()
    lit_counter = 0
    plain, restrictions = split_restrictions(g)
    for s, p, o in plain:
        sid = str(s)
        if sid not in added:
            net.add_node(sid, label=short(g, s), title=sid, shape="ellipse",
                         color="#cfe3ff")
            added.add(sid)

        if isinstance(o, Literal):
            lit_counter += 1           # one box per literal triple, like the W3C validator
            oid = f"literal-{lit_counter}"
            net.add_node(oid, label=short(g, o), shape="box", color="#ffe9b3")
        else:
            oid = str(o)
            if oid not in added:
                net.add_node(oid, label=short(g, o), title=oid, shape="ellipse",
                             color="#cfe3ff")
                added.add(oid)

        net.add_edge(sid, oid, label=short(g, p), title=str(p), arrows="to")

    # cardinality restrictions: one dashed red edge class -> property
    for cls, prop, label in restrictions:
        for term in (cls, prop):
            if str(term) not in added:
                net.add_node(str(term), label=short(g, term), title=str(term),
                             shape="ellipse", color="#cfe3ff")
                added.add(str(term))
        net.add_edge(str(cls), str(prop), label=label, arrows="to", dashes=True,
                     color="#d9534f", font={"color": "#d9534f", "size": 12},
                     title=f"{short(g, cls)} {label} {short(g, prop)}")

    net.write_html(str(out), notebook=False, open_browser=False)
    print(f"Wrote graph: {out}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Validate and visualise a Turtle file.")
    ap.add_argument("file", type=Path, help="path to a .ttl file")
    ap.add_argument("--no-open", action="store_true", help="don't open the HTML in a browser")
    args = ap.parse_args()

    if not args.file.exists():
        sys.exit(f"File not found: {args.file}")

    g = load(args.file)
    report(g)

    html_out = args.file.with_suffix(".html")
    write_html(g, html_out)

    if html_out.exists() and not args.no_open:
        webbrowser.open(html_out.resolve().as_uri())


if __name__ == "__main__":
    main()

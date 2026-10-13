"""Run an RML mapping and write the generated triples to a Turtle file.
One-time setup
python3 -m venv venv
source venv/bin/activate
pip install -r rml/requirements.txt

Usage (from anywhere):
    python rml/run_rml.py rml/mappings/parks.rml.ttl
    or whatever mapping you wanna run bud
"""
import argparse
import re
import sys
import tempfile
from pathlib import Path

import morph_kgc

RML_DIR = Path(__file__).resolve().parent


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mapping", help="RML mapping file (.ttl)")
    ap.add_argument("-s", "--source", help="CSV to use instead of the rml:source in the mapping")
    ap.add_argument("-o", "--output", help="output .ttl (default: rml/output/<mapping name>.ttl)")
    args = ap.parse_args()

    mapping = Path(args.mapping).resolve()
    if not mapping.is_file():
        sys.exit(f"Mapping not found: {mapping}")

    out = Path(args.output).resolve() if args.output else RML_DIR / "output" / (mapping.name.split(".")[0] + ".ttl")
    out.parent.mkdir(parents=True, exist_ok=True)

    text = mapping.read_text(encoding="utf-8")
    if args.source:
        source = Path(args.source).resolve()
        if not source.is_file():
            sys.exit(f"Source not found: {source}")
        text = re.sub(r'(rml:source\s+)"[^"]*"', lambda m: f'{m.group(1)}"{source}"', text)

    # Relative rml:source paths resolve against the working directory.
    import os
    os.chdir(RML_DIR)

    with tempfile.TemporaryDirectory() as tmp:
        tmp_mapping = Path(tmp) / "mapping.ttl"
        tmp_mapping.write_text(text, encoding="utf-8")
        config = f"[CONFIGURATION]\nlogging_level=ERROR\n[DataSource1]\nmappings={tmp_mapping}\n"
        graph = morph_kgc.materialize(config)

    graph.serialize(destination=str(out), format="turtle")
    print(f"{len(graph)} triples written to {out}")


if __name__ == "__main__":
    main()

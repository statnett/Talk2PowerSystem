#!/usr/bin/env python3
"""
add_iri.py — Annotate a PowSyBl SVG with iri= attributes from its metadata JSON.

For every SVG element whose id appears in the metadata JSON mapping, an `iri`
attribute is added whose value is the corresponding equipment mRID (optionally
expanded to a full IRI with --prefix).

Works with both NAD and SLD diagrams; the format is auto-detected from the JSON.

Usage:
    python3 add_iri.py diagram.svg [diagram.json] [--prefix NAMESPACE] [--inplace]

Examples:
    python3 add_iri.py svg/PowSyBl-NAD-LoadArea-NO-LA.svg
    python3 add_iri.py svg/PowSyBl-SLD-2substations-ARENDAL-and-KRISTIANSAND.svg \
        --prefix "http://my.cim.namespace/#"
    python3 add_iri.py svg/PowSyBl-NAD-LoadArea-NO-LA.svg --inplace
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from lxml import etree


_BUS_INDEX_SUFFIX = re.compile(r'_\d+$')
_SW_FICT_SUFFIX = re.compile(r'_SW_fict$')


def _normalize_mrid(mrid: str) -> str:
    """Remove _SW_fict suffix from mrids (fictitious switches)."""
    return _SW_FICT_SUFFIX.sub("", mrid)


def build_mapping_nad(meta: dict) -> dict[str, str]:
    """
    NAD JSON: entries in nodes/busNodes/edges/textNodes each have
    'svgId' (the SVG element id) and 'equipmentId' (the mRID).

    PowSyBl appends '_<index>' to the base mRID for busNodes (e.g.
    'abc123_0' for bus bar 0 of voltage level 'abc123').  That suffix
    is stripped here so the IRI always points to the real equipment mRID.
    """
    mapping: dict[str, str] = {}
    for section in ("nodes", "busNodes", "edges", "textNodes"):
        for item in meta.get(section, []):
            if "equipmentId" in item:
                mrid = item["equipmentId"]
                if section == "busNodes":
                    mrid = _BUS_INDEX_SUFFIX.sub("", mrid)
                mrid = _normalize_mrid(mrid)
                mapping[item["svgId"]] = mrid
    return mapping


def build_mapping_sld(meta: dict) -> dict[str, str]:
    """
    SLD JSON: entries in nodes have 'id' (= the SVG element id, hex-encoded)
    and 'equipmentId' (the mRID).  Only entries that have an equipmentId are
    real network elements; NODE / BUS_CONNECTION topology nodes have none.
    """
    mapping: dict[str, str] = {}
    for item in meta.get("nodes", []):
        if "equipmentId" in item:
            mapping[item["id"]] = _normalize_mrid(item["equipmentId"])
    return mapping


def detect_and_build_mapping(meta: dict) -> dict[str, str]:
    """Auto-detect NAD vs SLD by inspecting the first node entry."""
    nodes = meta.get("nodes", [])
    if nodes and "svgId" in nodes[0]:
        return build_mapping_nad(meta)
    return build_mapping_sld(meta)


def annotate_svg(svg_path: str, json_path: str, prefix: str, out_path: str) -> int:
    with open(json_path, encoding="utf-8") as f:
        meta = json.load(f)

    mapping = detect_and_build_mapping(meta)
    if not mapping:
        print(f"WARNING: no equipment mappings found in {json_path}", file=sys.stderr)

    parser = etree.XMLParser(remove_blank_text=False)
    tree = etree.parse(svg_path, parser)
    root = tree.getroot()

    count = 0
    for el in root.iter():
        eid = el.get("id")
        if eid and eid in mapping:
            el.set("iri", prefix + mapping[eid])
            count += 1

    tree.write(out_path, xml_declaration=False, encoding="utf-8", pretty_print=False)
    return count


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Add iri= attributes to a PowSyBl SVG from its metadata JSON."
    )
    parser.add_argument("svg", help="Input SVG file path")
    parser.add_argument(
        "json_file",
        nargs="?",
        default=None,
        help="Metadata JSON file (default: same path as SVG with .json extension)",
    )
    parser.add_argument(
        "--prefix",
        default="",
        help="Namespace prefix to prepend to each mRID (e.g. 'urn:uuid:')",
    )
    parser.add_argument(
        "--inplace",
        action="store_true",
        help="Overwrite the input SVG instead of writing a new .iri.svg file",
    )
    args = parser.parse_args()

    svg_path = args.svg
    if not os.path.isfile(svg_path):
        print(f"ERROR: SVG file not found: {svg_path}", file=sys.stderr)
        sys.exit(1)

    json_path = args.json_file or os.path.splitext(svg_path)[0] + ".json"
    if not os.path.isfile(json_path):
        print(f"ERROR: JSON file not found: {json_path}", file=sys.stderr)
        sys.exit(1)

    if args.inplace:
        out_path = svg_path
    else:
        base, ext = os.path.splitext(svg_path)
        out_path = base + ".iri" + ext

    count = annotate_svg(svg_path, json_path, args.prefix, out_path)
    print(f"Annotated {count} elements  ->  {out_path}")


if __name__ == "__main__":
    main()

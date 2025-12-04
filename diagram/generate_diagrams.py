#!/usr/bin/env python3
"""
Generate PowSyBl diagrams from specifications in diagrams.tsv

This script reads diagram specifications from diagrams.tsv and generates
SVG diagrams using pypowsybl, saving them to the svg/ folder.

Three diagram types are supported:
- NetworkAreaDiagram: Network area diagrams (full network or filtered by voltage levels)
- SingleLineDiagram: Single-line diagrams for individual substations
- SingleLineDiagram-Multi: Multi-substation single-line diagrams in matrix layout
"""

import os
import ast
import argparse
import pypowsybl.network as pn


def parse_mrids(mrids_str: str, kind: str) -> list | str | None:
    """
    Parse the mrids string from the TSV file based on diagram kind.
    
    Args:
        mrids_str: Raw mrids string from TSV (may have escaped quotes)
        kind: Diagram type (NetworkAreaDiagram, SingleLineDiagram, SingleLineDiagram-Multi)
    
    Returns:
        Parsed mrids in appropriate format for each diagram type
    """
    if not mrids_str or mrids_str.strip() == '':
        return None
    
    mrids_str = mrids_str.strip()
    
    if not mrids_str:
        return None
    
    if kind == "NetworkAreaDiagram":
        # Format: ("mrid1","mrid2",...) - tuple of voltage level IDs
        # Convert parentheses to brackets for ast.literal_eval
        if mrids_str.startswith('(') and mrids_str.endswith(')'):
            mrids_str = '[' + mrids_str[1:-1] + ']'
        return ast.literal_eval(mrids_str)
    
    elif kind == "SingleLineDiagram":
        # Format: "mrid" - single substation ID
        # Remove surrounding quotes if present
        if mrids_str.startswith('"') and mrids_str.endswith('"'):
            mrids_str = mrids_str[1:-1]
        return mrids_str
    
    elif kind == "SingleLineDiagram-Multi":
        # Format: [["mrid1","mrid2"]] - matrix of substation IDs
        return ast.literal_eval(mrids_str)
    
    return None


def read_tsv_with_escapes(tsv_path: str):
    """
    Read TSV file that uses backslash-quote escaping (like SPARQL output).
    
    Python's csv module expects double-quote escaping, so we need to 
    handle the backslash escaping ourselves.
    """
    rows = []
    with open(tsv_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    if not lines:
        return rows
    
    # Parse header
    header = lines[0].strip().split('\t')
    
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue
        
        # Split by tab, handling quoted fields with escaped quotes
        fields = []
        current_field = ''
        in_quotes = False
        i = 0
        
        while i < len(line):
            char = line[i]
            
            if char == '"' and not in_quotes:
                in_quotes = True
                i += 1
                continue
            elif char == '\\' and in_quotes and i + 1 < len(line) and line[i + 1] == '"':
                # Escaped quote - add the quote
                current_field += '"'
                i += 2
                continue
            elif char == '"' and in_quotes:
                in_quotes = False
                i += 1
                continue
            elif char == '\t' and not in_quotes:
                fields.append(current_field)
                current_field = ''
                i += 1
                continue
            else:
                current_field += char
                i += 1
        
        # Add the last field
        fields.append(current_field)
        
        # Create row dict
        row = {}
        for j, h in enumerate(header):
            row[h] = fields[j] if j < len(fields) else ''
        rows.append(row)
    
    return rows


def generate_diagrams(network_path: str, tsv_path: str, output_dir: str, verbose: bool = False):
    """
    Generate all diagrams specified in the TSV file.
    
    Args:
        network_path: Path to the CIM XML network file (zip)
        tsv_path: Path to the diagrams.tsv file
        output_dir: Directory to save SVG files
        verbose: Print progress information
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Load the network
    if verbose:
        print(f"Loading network from {network_path}...")
    network = pn.load(network_path)
    if verbose:
        print("Network loaded successfully.")
    
    # Set up SLD parameters for readable labels
    sld_params = pn.SldParameters(use_name=True)
    
    # Read and process the TSV file (with proper backslash-quote escaping)
    rows = read_tsv_with_escapes(tsv_path)
    
    success_count = 0
    error_count = 0
    
    for row in rows:
        kind = row.get('?kind', '').strip()
        mrids_raw = row.get('?mrids', '').strip()
        link = row.get('?link', '').strip()
        
        if not kind or not link:
            continue
        
        output_path = os.path.join(output_dir, link)
        
        try:
            mrids = parse_mrids(mrids_raw, kind)
            
            if kind == "NetworkAreaDiagram":
                if verbose:
                    print(f"Generating NetworkAreaDiagram: {link}")
                
                if mrids:
                    # NAD with specific voltage levels
                    network.write_network_area_diagram_svg(output_path, voltage_level_ids=mrids)
                else:
                    # Full network NAD
                    network.write_network_area_diagram_svg(output_path)
            
            elif kind == "SingleLineDiagram":
                if verbose:
                    print(f"Generating SingleLineDiagram: {link}")
                
                if mrids:
                    network.write_single_line_diagram_svg(mrids, output_path, parameters=sld_params)
            
            elif kind == "SingleLineDiagram-Multi":
                if verbose:
                    print(f"Generating SingleLineDiagram-Multi: {link}")
                
                if mrids:
                    network.write_matrix_multi_substation_single_line_diagram_svg(
                        mrids, output_path, parameters=sld_params
                    )
            
            else:
                if verbose:
                    print(f"Unknown diagram kind: {kind}")
                error_count += 1
                continue
            
            success_count += 1
            
        except Exception as e:
            print(f"Error generating {link}: {e}")
            error_count += 1
            # Remove empty file if it was created
            if os.path.exists(output_path) and os.path.getsize(output_path) == 0:
                os.remove(output_path)
    
    print(f"\nGeneration complete: {success_count} diagrams created, {error_count} errors")


def main():
    parser = argparse.ArgumentParser(
        description="Generate PowSyBl diagrams from TSV specifications"
    )
    parser.add_argument(
        '--network', '-n',
        default='/Users/tulechki/Projects/onto/statnett/Nordic44/instances/Grid/cimxml/Nordic44-HV_ALL',
        help='Path to the CIM XML network file (zip or directory)'
    )
    parser.add_argument(
        '--tsv', '-t',
        default=os.path.join(os.path.dirname(__file__), 'diagrams.tsv'),
        help='Path to the diagrams.tsv file'
    )
    parser.add_argument(
        '--output', '-o',
        default=os.path.join(os.path.dirname(__file__), 'svg'),
        help='Output directory for SVG files'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Print progress information'
    )
    
    args = parser.parse_args()
    
    generate_diagrams(args.network, args.tsv, args.output, args.verbose)


if __name__ == '__main__':
    main()


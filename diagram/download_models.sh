#!/bin/bash
# Download CIM XML models from a sources file and create a zip archive
#
# Usage: ./download_models.sh <sources_file> <output_zip>
# Example: ./download_models.sh sources-no44.txt nordic44.zip

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check arguments
if [[ $# -lt 2 ]]; then
    echo "Usage: $0 <sources_file> <output_zip>"
    echo "Example: $0 sources-no44.txt nordic44.zip"
    exit 1
fi

SOURCES_FILE="$1"
OUTPUT_ZIP="$2"

# Make paths absolute if relative
[[ "$SOURCES_FILE" != /* ]] && SOURCES_FILE="${SCRIPT_DIR}/${SOURCES_FILE}"
[[ "$OUTPUT_ZIP" != /* ]] && OUTPUT_ZIP="${SCRIPT_DIR}/${OUTPUT_ZIP}"

TEMP_DIR="${SCRIPT_DIR}/.download_temp_$$"

# Verify sources file exists
if [[ ! -f "$SOURCES_FILE" ]]; then
    echo "Error: Sources file not found: $SOURCES_FILE"
    exit 1
fi

# Clean up temp directory on exit
cleanup() {
    rm -rf "$TEMP_DIR"
}
trap cleanup EXIT

# Create temp directory
mkdir -p "$TEMP_DIR"

# Remove existing zip if present
rm -f "$OUTPUT_ZIP"

echo "Downloading models from $(basename "$SOURCES_FILE")..."
echo "======================================="

success_count=0
skip_count=0
error_count=0

# Track downloaded files to avoid duplicates (using a simple file list)
downloaded_list=""

while IFS= read -r url || [[ -n "$url" ]]; do
    # Skip empty lines
    [[ -z "$url" ]] && continue
    
    # Extract filename from URL
    filename=$(basename "$url")
    
    # Skip if already downloaded (handle duplicates in sources file)
    if echo "$downloaded_list" | grep -q "|${filename}|"; then
        echo "⊘ Skipping duplicate: $filename"
        ((skip_count++))
        continue
    fi
    
    echo -n "Downloading $filename... "
    
    # Download file
    http_code=$(curl -skL -w "%{http_code}" -o "$TEMP_DIR/$filename" "$url" 2>/dev/null)
    
    if [[ "$http_code" == "200" ]]; then
        echo "✓"
        downloaded_list="${downloaded_list}|${filename}|"
        ((success_count++))
    else
        echo "✗ (HTTP $http_code)"
        rm -f "$TEMP_DIR/$filename"
        ((error_count++))
    fi
done < "$SOURCES_FILE"

echo ""
echo "Creating $(basename "$OUTPUT_ZIP")..."

# Create zip archive from all downloaded files
cd "$TEMP_DIR"
file_count=$(ls -1 *.xml 2>/dev/null | wc -l | tr -d ' ')
if [[ "$file_count" -gt 0 ]]; then
    zip -q "$OUTPUT_ZIP" *.xml
    echo "✓ Created $OUTPUT_ZIP"
else
    echo "✗ No files to add to archive"
    exit 1
fi

echo ""
echo "======================================="
echo "Summary:"
echo "  Downloaded: $success_count files"
echo "  Skipped (duplicates): $skip_count files"
echo "  Errors: $error_count files"
echo ""
echo "Output: $OUTPUT_ZIP"

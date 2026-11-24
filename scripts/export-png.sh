#!/usr/bin/env bash
# Rasterize SVG icons in apps/, kinds/, and providers/ to PNG.
# Writes 128 px and 512 px PNGs to <folder>/png/<name>-<size>.png.

set -euo pipefail

# Ensure we run from repository root
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

# Default configuration
FOLDERS=("apps" "kinds" "providers")
SIZES=(128 512)
ENGINE="${ENGINE:-}"

# Parse optional arguments
show_help() {
  cat <<'EOF'
Usage: ./scripts/export-png.sh [OPTIONS] [FOLDER...]

Export 128 px and 512 px PNGs for each SVG in apps/, kinds/, and providers/
into <folder>/png/<name>-<size>.png.

Arguments:
  FOLDER...             Specific folder(s) to process (default: apps kinds providers)

Options:
  -e, --engine <name>   Rasterizer to use: rsvg-convert or resvg (default: auto-detect)
  -s, --sizes <sizes>   Comma-separated sizes (default: 128,512)
  -h, --help            Show this help message
EOF
}

CUSTOM_FOLDERS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help)
      show_help
      exit 0
      ;;
    -e|--engine)
      ENGINE="$2"
      shift 2
      ;;
    -s|--sizes)
      IFS=',' read -r -a SIZES <<< "$2"
      shift 2
      ;;
    -*)
      echo "Error: Unknown option $1" >&2
      show_help >&2
      exit 1
      ;;
    *)
      CUSTOM_FOLDERS+=("$1")
      shift
      ;;
  esac
done

if [[ ${#CUSTOM_FOLDERS[@]} -gt 0 ]]; then
  FOLDERS=("${CUSTOM_FOLDERS[@]}")
fi

# Detect available rasterizer
if [[ -z "$ENGINE" ]]; then
  if command -v rsvg-convert >/dev/null 2>&1; then
    ENGINE="rsvg-convert"
  elif command -v resvg >/dev/null 2>&1; then
    ENGINE="resvg"
  else
    echo "Error: No supported SVG rasterizer found in PATH." >&2
    echo "Please install 'rsvg-convert' (librsvg) or 'resvg':" >&2
    echo "  - macOS: brew install librsvg" >&2
    echo "  - Debian/Ubuntu: sudo apt-get install librsvg2-bin" >&2
    echo "  - Arch: sudo pacman -S librsvg" >&2
    echo "  - Windows (winget): winget install linebender.resvg" >&2
    echo "  - Cargo: cargo install resvg" >&2
    exit 1
  fi
fi

# Validate engine
case "$ENGINE" in
  rsvg-convert)
    if ! command -v rsvg-convert >/dev/null 2>&1; then
      echo "Error: 'rsvg-convert' not found in PATH." >&2
      exit 1
    fi
    ;;
  resvg)
    if ! command -v resvg >/dev/null 2>&1; then
      echo "Error: 'resvg' not found in PATH." >&2
      exit 1
    fi
    ;;
  *)
    echo "Error: Unsupported engine '$ENGINE'. Use 'rsvg-convert' or 'resvg'." >&2
    exit 1
    ;;
esac

echo "Using rasterizer: $ENGINE"
echo "Target folders: ${FOLDERS[*]}"
echo "Target sizes: ${SIZES[*]}"

count=0

rasterize() {
  local svg="$1"
  local size="$2"
  local out="$3"

  mkdir -p "$(dirname "$out")"
  case "$ENGINE" in
    rsvg-convert)
      rsvg-convert -w "$size" -h "$size" "$svg" -o "$out"
      ;;
    resvg)
      resvg --quiet -w "$size" -h "$size" "$svg" "$out"
      ;;
  esac
}

for folder in "${FOLDERS[@]}"; do
  if [[ ! -d "$folder" ]]; then
    echo "Warning: Directory '$folder' does not exist, skipping." >&2
    continue
  fi

  shopt -s nullglob
  svgs=("$folder"/*.svg)
  shopt -u nullglob

  if [[ ${#svgs[@]} -eq 0 ]]; then
    continue
  fi

  for svg in "${svgs[@]}"; do
    filename="$(basename "$svg")"
    name="${filename%.svg}"

    for size in "${SIZES[@]}"; do
      out="$folder/png/$name-$size.png"
      rasterize "$svg" "$size" "$out"
      count=$((count + 1))
    done
  done
done

echo "Successfully exported $count PNGs to the selected folders' png/ directories."

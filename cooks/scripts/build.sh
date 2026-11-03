#!/usr/bin/env bash
# Rebuilds everything in cooks/ from the Run My Agents avatar code.
#   scripts/build.sh /path/to/run-my-agents
# Needs bun, rsvg-convert (librsvg) and python3. The cooks (SVG, PNG, 3D) are written next to this script's folder.
set -euo pipefail
src="${1:?usage: build.sh /path/to/run-my-agents}"
here="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$here/svg" "$here/png" "$here/face" "$here/3d"
bun "$here/scripts/export-svg.ts" "$src" "$here"
for f in "$here"/svg/*.svg; do
  n="$(basename "$f" .svg)"
  for z in 32 64 128 512; do rsvg-convert -w "$z" -h "$z" "$f" -o "$here/png/$n-$z.png"; done
done
for f in "$here"/face/*.svg; do rsvg-convert -w 512 -h 512 "$f" -o "${f%.svg}.png"; done
python3 -I "$here/scripts/build-glb.py" "$here"

#!/usr/bin/env python3
"""Check that README.md publishes every app and kind icon in the repo.

Run from the repo root: python3 scripts/check_emoji_readme.py
The check exits 1 with one line per problem so a missing icon is easy to spot in CI.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

SIZES = (512, 128, 64, 32)
ICON_LINK = re.compile(r"\]\((?:\./)?((?:apps|kinds)/[A-Za-z0-9_./-]+\.(?:svg|png))\)")


def strip_block(readme: str, section: str) -> str:
    """The paragraph of 40 px images that opens a section's table."""
    marker = f'<img src="{section}/png/'
    start = readme.find(marker)
    if start < 0:
        return ""
    end = readme.find("</p>", start)
    return readme[start:end] if end >= 0 else ""


def check(root: Path) -> list[str]:
    readme = (root / "README.md").read_text(encoding="utf-8")
    links = set(ICON_LINK.findall(readme))
    problems: list[str] = []

    for section in ("apps", "kinds"):
        svg_dir = root / section
        strip = strip_block(readme, section)
        for svg in sorted(svg_dir.glob("*.svg")):
            name = svg.stem
            if f"{section}/{name}.svg" not in links:
                problems.append(f"{section}/{name}.svg is not listed in README.md")
            if f'{section}/png/{name}-64.png" width="40"' not in strip:
                problems.append(f"{section}/png/{name}-64.png is missing from the README strip")
            for size in SIZES:
                png = svg_dir / "png" / f"{name}-{size}.png"
                if not png.is_file():
                    problems.append(f"missing {section}/png/{name}-{size}.png")
                elif f"{section}/png/{name}-{size}.png" not in links:
                    problems.append(f"{section}/png/{name}-{size}.png is not linked in README.md")

    # Both download links and inline thumbnails must resolve.
    for path in sorted(links):
        if not (root / path).is_file():
            problems.append(f"README links a missing file: {path}")
    for token in readme.split('src="'):
        path = token.split('"', 1)[0]
        if (path.startswith("apps/") or path.startswith("kinds/")) and not (root / path).is_file():
            problems.append(f"README links a missing file: {path}")
    return problems


def main() -> int:
    problems = check(Path(__file__).resolve().parent.parent)
    if problems:
        for problem in problems:
            print(problem)
        return 1
    print("README publishes every app and kind icon")
    return 0


if __name__ == "__main__":
    sys.exit(main())

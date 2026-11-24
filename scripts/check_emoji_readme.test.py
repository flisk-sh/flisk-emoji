"""Unit tests for check_emoji_readme.check."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from check_emoji_readme import check


def fixture(readme: str, *, with_pngs: bool = True) -> Path:
    root = Path(tempfile.mkdtemp())
    (root / "apps").mkdir()
    (root / "apps" / "citable.svg").write_text("<svg></svg>", encoding="utf-8")
    (root / "apps" / "cilytics.svg").write_text("<svg></svg>", encoding="utf-8")
    if with_pngs:
        (root / "apps" / "png").mkdir()
        for name in ("citable", "cilytics"):
            for size in (512, 128, 64, 32):
                (root / "apps" / "png" / f"{name}-{size}.png").write_bytes(b"png")
    (root / "README.md").write_text(readme, encoding="utf-8")
    return root


def full_readme() -> str:
    rows = []
    strip = []
    for name in ("citable", "cilytics"):
        strip.append(f'<img src="apps/png/{name}-64.png" width="40" alt="{name}">')
        rows.append(
            f'| <img src="apps/png/{name}-64.png" width="28" alt="{name}"> | {name} | '
            f'[{name}.svg](apps/{name}.svg), '
            + ", ".join(
                f'[{s}](apps/png/{name}-{s}.png)' for s in (512, 128, 64, 32)
            )
            + " |"
        )
    return "<p>" + " ".join(strip) + "</p>\n" + "\n".join(rows)


class EmojiReadmeTest(unittest.TestCase):
    def test_every_app_is_published(self) -> None:
        self.assertEqual(check(fixture(full_readme())), [])

    def test_missing_app_row_is_reported(self) -> None:
        root = fixture(full_readme().replace("apps/cilytics.svg", "apps/wrong.svg"))
        problems = check(root)
        self.assertTrue(any("cilytics.svg is not listed" in p for p in problems))

    def test_missing_strip_image_is_reported(self) -> None:
        readme = full_readme().replace(
            '<img src="apps/png/cilytics-64.png" width="40" alt="cilytics">', ""
        )
        problems = check(fixture(readme))
        self.assertTrue(any("cilytics-64.png is missing from the README strip" in p for p in problems))

    def test_missing_png_file_is_reported(self) -> None:
        problems = check(fixture(full_readme(), with_pngs=False))
        self.assertTrue(any("missing apps/png/citable-512.png" in p for p in problems))

    def test_broken_download_link_is_reported_even_when_the_thumbnail_exists(self) -> None:
        readme = full_readme().replace(
            "[64](apps/png/citable-64.png)", "[64](apps/png/citable-65.png)"
        )
        problems = check(fixture(readme))
        self.assertIn("apps/png/citable-64.png is not linked in README.md", problems)
        self.assertIn("README links a missing file: apps/png/citable-65.png", problems)

    def test_plain_svg_path_does_not_count_as_a_link(self) -> None:
        readme = full_readme().replace("[citable.svg](apps/citable.svg)", "`apps/citable.svg`")
        self.assertIn("apps/citable.svg is not listed in README.md", check(fixture(readme)))


if __name__ == "__main__":
    unittest.main()

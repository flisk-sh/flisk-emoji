"""Test that the rasterizer updates the PNGs published by the README."""
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


class ExportPngTest(unittest.TestCase):
    def test_exports_to_each_icons_published_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "scripts").mkdir()
            script = shutil.copy(Path(__file__).with_name("export-png.sh"), root / "scripts")
            folders = ("apps", "kinds", "providers")
            for folder in folders:
                (root / folder).mkdir()
                (root / folder / "sample.svg").write_text("<svg/>", encoding="utf-8")

            rasterizer = root / "rsvg-convert"
            rasterizer.write_text(
                '#!/bin/sh\nset -eu\n[ "$6" = "-o" ]\nprintf "%s\\n" "$2" > "$7"\n',
                encoding="utf-8",
            )
            rasterizer.chmod(0o755)

            subprocess.run(
                ["bash", script, "--engine", "rsvg-convert"],
                env={**os.environ, "PATH": str(root) + os.pathsep + os.environ["PATH"]},
                check=True,
                capture_output=True,
            )

            expected = {
                root / folder / "png" / f"sample-{size}.png": f"{size}\n"
                for folder in folders
                for size in (128, 512)
            }
            self.assertEqual(set(root.rglob("*.png")), set(expected))
            for path, content in expected.items():
                self.assertEqual(path.read_text(encoding="utf-8"), content)


if __name__ == "__main__":
    unittest.main()

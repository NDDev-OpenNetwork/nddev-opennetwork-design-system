"""Exercise the generator's drift gate without touching checked-in projections."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

import generate_tokens


class TokenGenerationTest(unittest.TestCase):
    def test_check_rejects_projection_drift_without_repairing_it(self):
        source = (generate_tokens.ROOT / "tokens/tokens.json").read_text()
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "tokens").mkdir()
            (root / "packages/flutter/lib/src").mkdir(parents=True)
            (root / "tools").mkdir()
            (root / "tokens/tokens.json").write_text(source)
            script = root / "tools/generate_tokens.py"
            shutil.copyfile(generate_tokens.__file__, script)
            command = [sys.executable, "-B", str(script)]
            subprocess.run(command, check=True, capture_output=True, timeout=5)
            subprocess.run(command + ["--check"], check=True, capture_output=True, timeout=5)
            for relative in ["tokens/tokens.css", "packages/flutter/lib/src/tokens.dart"]:
                path = root / relative
                original = path.read_text()
                path.write_text(original + "// manual edit\n")
                result = subprocess.run(command + ["--check"], capture_output=True, text=True, timeout=5)
                self.assertEqual(result.returncode, 1)
                self.assertIn(relative, result.stderr)
                self.assertTrue(path.read_text().endswith("// manual edit\n"))
                path.write_text(original)

    def test_invalid_source_rejected(self):
        data = json.loads((generate_tokens.ROOT / "tokens/tokens.json").read_text())
        for value in ["red", "#GGGGGG", "#123456; color: red"]:
            with self.subTest(value=value):
                data["color"]["focus-ring"]["$value"] = value
                with self.assertRaises(ValueError):
                    generate_tokens.render(data)


if __name__ == "__main__":
    unittest.main()

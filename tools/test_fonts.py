"""Verify the actual redistributable font payload and license, without network."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class FontPayload(unittest.TestCase):
    def test_bundled_fonts_and_license_match_reviewed_ibm_source(self):
        source = json.loads((ROOT / 'assets/font-source.json').read_text())
        fonts = ROOT / 'packages/flutter/assets/fonts'
        self.assertEqual({f['weight'] for f in source['files']}, {400, 500, 600})
        self.assertEqual({p.name for p in fonts.glob('*.ttf')},
                         {f['file'] for f in source['files']})
        for record in source['files']:
            data = (fonts / record['file']).read_bytes()
            self.assertEqual(data[:4], b'\x00\x01\x00\x00')
            self.assertEqual(hashlib.sha256(data).hexdigest(), record['sha256'])
            self.assertTrue(record['url'].startswith('https://fonts.gstatic.com/s/ibmplexsans/'))
        license = (fonts / 'OFL.txt').read_bytes()
        self.assertIn(b'SIL OPEN FONT LICENSE', license)
        self.assertEqual(hashlib.sha256(license).hexdigest(), source['license_sha256'])

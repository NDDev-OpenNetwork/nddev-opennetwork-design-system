import unittest
from PIL import Image
import io
from generate_launchers import png, render

class LauncherContract(unittest.TestCase):
    def test_native_dimensions_opaque_corners_and_visible_mark(self):
        for size in [16, 48, 256, 1024]:
            with self.subTest(size=size):
                image = render(size)
                self.assertEqual(image.size, (size, size))
                self.assertEqual(image.mode, 'RGB')
                self.assertEqual(image.getpixel((0, 0)), (7, 10, 18))
                # Small launcher sizes retain contrast without filling the background.
                foreground = [pixel for pixel in image.get_flattened_data() if pixel[0] > 50 and pixel[1] > 100 and pixel[2] > 150]
                self.assertGreater(len(foreground), size * size // 20)
                self.assertLess(len(foreground), size * size // 2)
                self.assertEqual(Image.open(io.BytesIO(png(size))).size, (size, size))

    def test_renderer_rejects_unbounded_dimensions(self):
        for size in [0, 15, 1025, 100000]:
            with self.assertRaises(ValueError): render(size)

class ProvenanceContract(unittest.TestCase):
    def test_committed_bytes_and_inventory_are_both_required(self):
        import json
        from pathlib import Path
        from tempfile import TemporaryDirectory
        from generate_launchers import assets, digest, verify, CANONICAL_RENDERER
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'module.yaml').write_text('id: mobile\n')
            icons = root / 'ios/Runner/Assets.xcassets/AppIcon.appiconset'
            icons.mkdir(parents=True)
            (icons / 'Contents.json').write_text(json.dumps({'images': [
                {'filename': 'icon.png', 'size': '40x40', 'scale': '1x'}]}))
            generated = assets(root, 'mobile')
            for name, data in generated.items():
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
            source = {'renderer': CANONICAL_RENDERER, 'inputs_sha256': {}}
            record = {'source': source, 'files_sha256': {
                name: digest(data) for name, data in generated.items()}}
            provenance = root / 'generated/launcher-provenance.json'
            provenance.parent.mkdir()
            provenance.write_text(json.dumps(record))
            self.assertEqual(verify(root, 'mobile', source), len(generated))
            name = next(iter(generated))
            (root / name).write_bytes(generated[name] + b'changed')
            with self.assertRaisesRegex(ValueError, 'Committed launcher bytes'):
                verify(root, 'mobile', source)
            (root / name).write_bytes(generated[name])
            record['files_sha256']['../outside.png'] = '0' * 64
            provenance.write_text(json.dumps(record))
            with self.assertRaisesRegex(ValueError, 'inventory'):
                verify(root, 'mobile', source)
            del record['files_sha256']['../outside.png']
            record['source'] = {'renderer': 'unreviewed'}
            provenance.write_text(json.dumps(record))
            with self.assertRaisesRegex(ValueError, 'source/input/renderer'):
                verify(root, 'mobile', source)

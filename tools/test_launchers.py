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

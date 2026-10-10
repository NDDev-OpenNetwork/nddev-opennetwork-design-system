#!/usr/bin/env python3
"""Render native launcher assets from the canonical NDDev mark and design tokens."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET

import PIL
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
INPUTS = ['assets/nddev-mark.svg', 'assets/brand-source.json', 'tokens/tokens.json', 'tools/generate_launchers.py']
RENDERER_VERSION = '12.1.1'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def render(size):
    if PIL.__version__ != RENDERER_VERSION:
        raise ValueError('Install the pinned requirements-icons.txt renderer')
    if not 16 <= size <= 1024:
        raise ValueError('Launcher dimension must be 16..1024')
    source = json.loads((ROOT / 'assets/brand-source.json').read_text())
    svg = (ROOT / 'assets/nddev-mark.svg').read_bytes()
    if digest(svg) != source['svg_sha256']:
        raise ValueError('Canonical mark differs from its reviewed source')
    tokens = json.loads((ROOT / 'tokens/tokens.json').read_text())
    def color(key):
        group, name = source[key].split('.')
        return tokens[group][name]['$value']
    mark = ET.fromstring(svg)
    if mark.tag != '{http://www.w3.org/2000/svg}svg' or mark.get('viewBox') != '0 0 165.36 165.19':
        raise ValueError('Unsupported canonical SVG profile')
    # Native launcher safe area: the unchanged mark fits within 66/108 of the
    # square, leaving room for platform masks. Supersampling preserves edges.
    scale = size * 4
    image = Image.new('RGB', (scale, scale), color('background_token'))
    draw = ImageDraw.Draw(image)
    ratio = scale * (66 / 108) / 165.36
    offset = ((scale - 165.36 * ratio) / 2, (scale - 165.19 * ratio) / 2)
    if len(mark) != 3:
        raise ValueError('Expected the three reviewed polygons')
    for polygon in mark:
        if polygon.tag != '{http://www.w3.org/2000/svg}polygon' or set(polygon.attrib) != {'points'}:
            raise ValueError('Unsupported canonical SVG element')
        values = [float(value) for value in polygon.attrib['points'].split()]
        if len(values) % 2 or len(values) > 64:
            raise ValueError('Invalid bounded polygon')
        points = [(x * ratio + offset[0], y * ratio + offset[1]) for x, y in zip(values[::2], values[1::2])]
        draw.polygon(points, fill=color('foreground_token'))
    return image.resize((size, size), Image.Resampling.LANCZOS)


def png(size):
    output = io.BytesIO()
    render(size).save(output, format='PNG', compress_level=9, optimize=False)
    return output.getvalue()


def assets(root, platform):
    if f'id: {platform}\n' not in (root / 'module.yaml').read_text():
        raise ValueError('Destination is not the declared NDS runner repository')
    result = {}
    apple = 'macos' if platform == 'desktop' else 'ios'
    icons = Path(apple) / 'Runner/Assets.xcassets/AppIcon.appiconset'
    for item in json.loads((root / icons / 'Contents.json').read_text())['images']:
        if 'filename' not in item:
            continue
        if Path(item['filename']).name != item['filename'] or not item['filename'].endswith('.png'):
            raise ValueError('Expected a local PNG filename in the launcher manifest')
        size = round(float(item['size'].split('x')[0]) * float(item['scale'].removesuffix('x')))
        result[str(icons / item['filename'])] = png(size)
    if platform == 'desktop':
        output = io.BytesIO()
        render(256).save(output, format='ICO', sizes=[(v, v) for v in [16, 24, 32, 48, 64, 128, 256]])
        result['windows/runner/resources/app_icon.ico'] = output.getvalue()
        result['linux/runner/resources/app_icon.png'] = png(256)
    else:
        for density, size in [('mdpi', 48), ('hdpi', 72), ('xhdpi', 96), ('xxhdpi', 144), ('xxxhdpi', 192)]:
            result[f'android/app/src/main/res/mipmap-{density}/ic_launcher.png'] = png(size)
    return result


def source_identity():
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    hashes = {}
    for name in INPUTS:
        content = (ROOT / name).read_bytes()
        published = subprocess.check_output(['git', 'show', f'{commit}:{name}'], cwd=ROOT)
        if content != published:
            raise ValueError('Launcher generation requires committed canonical inputs')
        hashes[name] = digest(content)
    return {'repository': 'NDDev-OpenNetwork/nddev-opennetwork-design-system',
            'commit': commit, 'inputs_sha256': hashes, 'pillow_version': RENDERER_VERSION}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--desktop', type=Path)
    parser.add_argument('--mobile', type=Path)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    if not args.desktop and not args.mobile:
        parser.error('An existing desktop or mobile runner repository is required')
    source = source_identity()
    for platform in ['desktop', 'mobile']:
        root = getattr(args, platform)
        if root is None:
            continue
        generated = assets(root, platform)
        record = {'source': source, 'files_sha256': {name: digest(data) for name, data in sorted(generated.items())}}
        generated['generated/launcher-provenance.json'] = (json.dumps(record, indent=2, sort_keys=True) + '\n').encode()
        for name, data in generated.items():
            path = root / name
            if args.check:
                if not path.is_file() or path.read_bytes() != data:
                    raise SystemExit(f'Launcher drift: {name}')
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
        print(f'{platform}: {len(generated)-1} launcher assets verified' if args.check else f'{platform}: {len(generated)-1} launcher assets generated')

if __name__ == '__main__':
    main()

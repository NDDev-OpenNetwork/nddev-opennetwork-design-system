#!/usr/bin/env python3
"""Project the authentic SVG polygons into a native Flutter Path."""
import argparse
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def render():
    blob = (ROOT / 'assets/nddev-mark.svg').read_bytes()
    source = json.loads((ROOT / 'assets/brand-source.json').read_text())
    if hashlib.sha256(blob).hexdigest() != source['svg_sha256']:
        raise ValueError('Canonical mark source drift')
    svg = ET.fromstring(blob)
    if svg.get('viewBox') != '0 0 165.36 165.19' or len(svg) != 3:
        raise ValueError('Unexpected canonical mark geometry')
    lines = ["// Generated from assets/nddev-mark.svg; run just tokens. Do not edit.",
             "import 'package:flutter/painting.dart';", '',
             'const nddevMarkSize = Size(165.36, 165.19);', '',
             'Path nddevMarkPath() => Path()']
    for polygon in svg:
        if polygon.tag != '{http://www.w3.org/2000/svg}polygon' or set(polygon.attrib) != {'points'}:
            raise ValueError('Unexpected SVG element')
        values = [float(v) for v in polygon.attrib['points'].split()]
        for index in range(0, len(values), 2):
            command = 'moveTo' if index == 0 else 'lineTo'
            lines.append(f'  ..{command}({values[index]:g}, {values[index + 1]:g})')
        lines.append('  ..close()')
    lines[-1] += ';'
    return '\n'.join(lines) + '\n'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = render()
    path = ROOT / 'packages/flutter/lib/src/brand_geometry.dart'
    if args.check:
        if path.read_text() != result:
            raise SystemExit('Native brand geometry differs; run just tokens')
    else:
        path.write_text(result)

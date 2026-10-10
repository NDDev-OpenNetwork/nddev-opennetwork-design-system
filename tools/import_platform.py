#!/usr/bin/env python3
"""Export only OpenNetwork visual tokens from a reviewed platform checkout."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
INPUTS = ('design/tokens.json', 'src/styles/tokens.generated.css',
          'src/styles/primitives.css', 'src/styles/base.css', 'src/assets/brand/nddev.svg')


def token(kind, value):
    return {'$type': kind, '$value': value}


def export(source):
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=source, text=True).strip()
    hashes = {}
    for name in INPUTS:
        data = (source / name).read_bytes()
        if data != subprocess.check_output(['git', 'show', f'{commit}:{name}'], cwd=source):
            raise ValueError('Commit the reviewed platform design inputs first')
        hashes[name] = hashlib.sha256(data).hexdigest()
    # The platform owns color derivation and its contrast policy.
    subprocess.run(['node', str(source / 'scripts/generate-tokens.mjs'), '--check'],
                   cwd=source, check=True, timeout=30, capture_output=True)
    data = json.loads((source / INPUTS[0]).read_text())
    def geometry(path):
        svg = ET.parse(path).getroot()
        return svg.get('viewBox'), [node.attrib['points'].split() for node in svg]
    if geometry(source / INPUTS[-1]) != geometry(ROOT / 'assets/nddev-mark.svg'):
        raise ValueError('The native mark must preserve platform geometry')
    css = (source / INPUTS[1]).read_text()
    blocks = [(selector.strip(), dict(re.findall(r'--([\w-]+):\s*([^;]+);', body)))
              for selector, body in re.findall(r'([^{}]+)\{([^{}]+)\}', css)]

    def colors(light):
        neutral = next(values for selector, values in blocks
                       if '--surface-base' not in selector and 'surface-base' in values
                       and (selector == "[data-theme='light']") == light)
        accent = next(values for selector, values in blocks
                      if "[data-direction='on']" in selector
                      and ("[data-theme='light']" in selector) == light)
        selected = {k: v for k, v in neutral.items() if
                    k.startswith(('surface-', 'text-primary', 'text-secondary',
                                  'text-tertiary', 'border-', 'focus-')) or
                    re.fullmatch(r'status-(success|warning|danger|info)-(text|border|subtle)', k)}
        selected.update({k: v for k, v in accent.items() if k.startswith('accent-')
                         and not k.startswith(('accent-closing-', 'accent-crosslink-'))})
        if any(not re.fullmatch('#[0-9A-Fa-f]{6}', v) for v in selected.values()):
            raise ValueError('Expected resolved OpenNetwork colors')
        return {k: token('color', v) for k, v in selected.items()}

    def pixels(value):
        if value.endswith('rem'):
            return f'{float(value[:-3]) * 16:g}px'
        if re.fullmatch(r'[0-9.]+px', value):
            return value
        raise ValueError('Expected an absolute interface dimension')

    font = re.search(r"--font-sans:\s*'([^']+)'", (source / 'src/styles/base.css').read_text())
    if font is None or font[1] != 'IBM Plex Sans':
        raise ValueError('Review the bundled native fonts for this platform family')
    typography = {
        'font-family': token('fontFamily', font[1] + ', sans-serif'),
        'viewport-min': token('dimension', f"{data['type']['viewport_px'][0]}px"),
        'viewport-max': token('dimension', f"{data['type']['viewport_px'][1]}px"),
    }
    for role, (minimum, maximum) in data['type']['scale_px'].items():
        typography[role + '-min'] = token('dimension', f'{minimum}px')
        typography[role + '-max'] = token('dimension', f'{maximum}px')
        typography[role + '-leading'] = token('number', data['type']['line_height'][role])
    for role, value in data['type']['weight'].items():
        typography['weight-' + role] = token('number', value)
    return {
        '$schema': 'https://schemas.figma.com/w3c-design-tokens.schema.json',
        '$extensions': {'nddev': {'source_url': 'https://nddev.ai/opennetwork/en',
                                 'source_commit': commit, 'inputs_sha256': hashes,
                                 'direction': 'on', 'default_theme': data['default_theme'],
                                 'rem_to_logical_pixels': 16}},
        'color': colors(False), 'light-color': colors(True),
        'space': {k: token('dimension', f'{v * 16:g}px') for k, v in data['space_rem'].items()},
        'radius': {('xxl' if k == '2xl' else k): token('dimension', pixels(v)) for k, v in data['radius'].items()},
        'size': {k: token('dimension', pixels(v)) for k, v in data['size'].items()
                 if k in ('target-min', 'control-md', 'control-lg', 'field', 'icon', 'icon-md', 'brand', 'dock-tile')},
        'typography': typography,
        'motion': {'ui-fast': token('number', data['motion']['ui_ms'][0]),
                   'ui': token('number', data['motion']['ui_ms'][1])},
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    rendered = json.dumps(export(args.source.resolve()), indent=2) + '\n'
    path = ROOT / 'tokens/tokens.json'
    if args.check:
        if path.read_text() != rendered:
            raise SystemExit('OpenNetwork export differs from the reviewed platform source')
    else:
        path.write_text(rendered)
    print('OpenNetwork-only platform token export verified' if args.check else 'Exported OpenNetwork tokens')

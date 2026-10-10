#!/usr/bin/env python3
"""Generate the CSS and Flutter projections of the canonical design tokens."""

import argparse
import json
import math
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
GROUPS = {
    "space": "Spacing",
    "radius": "Radii",
    "size": "Sizes",
    "typography": "Typography",
    "motion": "Motion",
}
# Preserve the published spacing names.
SPACING_NAMES = {
    "0": "zero", "1": "one", "2": "two", "3": "three", "4": "four",
    "6": "six", "8": "eight", "12": "twelve", "16": "sixteen", "24": "twentyFour",
}


def identifier(group, name):
    if group == "space":
        return SPACING_NAMES.get(name, f"space{name}")
    head, *tail = name.split("-")
    return head + "".join(part.capitalize() for part in tail)


def project(token):
    kind, value = token["$type"], token["$value"]
    if kind == "color" and isinstance(value, str) and re.fullmatch(r"#[0-9a-fA-F]{6}", value):
        return value.lower(), f"Color(0xFF{value[1:].upper()})"
    if kind == "dimension" and isinstance(value, str) and re.fullmatch(r"(?:0|[1-9][0-9]*)(?:\.[0-9]+)?px", value):
        return value, str(float(value[:-2]))
    if kind == "number" and type(value) in (int, float) and math.isfinite(value) and value > 0:
        return str(value), str(float(value))
    if kind == "fontFamily" and isinstance(value, str) and re.fullmatch(r"[a-zA-Z][a-zA-Z0-9 ,\-]*", value):
        families = [family.strip() for family in value.split(",")]
        if all(families):
            return value, "<String>[" + ", ".join(repr(family) for family in families) + "]"
    raise ValueError(f"Unsupported or invalid token: {token!r}")


def render(data):
    if set(data) - {"$schema", "$extensions", "color", "light-color"} != set(GROUPS):
        raise ValueError("Unexpected token groups")
    if set(data['color']) != set(data['light-color']):
        raise ValueError("Both themes must implement the same color roles")
    notice = "Generated from tokens/tokens.json; run just tokens. Do not edit."
    css = [f"/* {notice} */"]
    dart = [f"// {notice}", "", "import 'package:flutter/material.dart';", ""]
    dart.extend(['class OpenNetworkPalette {', '  const OpenNetworkPalette({'])
    for name in data['color']:
        dart.append(f'    required this.{identifier("color", name)},')
    dart.append('  });')
    for name in data['color']:
        dart.append(f'  final Color {identifier("color", name)};')
    dart.extend(['}', '', 'abstract final class OpenNetworkColors {'])
    for group, theme, selector in [('color', 'dark', ":root, [data-theme='dark']"),
                                   ('light-color', 'light', "[data-theme='light']")]:
        css.append(selector + ' {')
        dart.append(f'  static const {theme} = OpenNetworkPalette(')
        for name, token in data[group].items():
            if not re.fullmatch(r'[a-z]+(?:-[a-z]+)*', name) or token['$type'] != 'color':
                raise ValueError('Invalid color role')
            css_value, dart_value = project(token)
            css.append(f'  --on-color-{name}: {css_value};')
            dart.append(f'    {identifier(group, name)}: {dart_value},')
        css.extend(['}', ''])
        dart.append('  );')
    dart.extend(['}', ''])
    css.append(':root {')
    for group, class_name in GROUPS.items():
        dart.append(f"abstract final class OpenNetwork{class_name} {{")
        names = set()
        for name, token in data[group].items():
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
                raise ValueError(f"Invalid token name: {group}.{name}")
            field = identifier(group, name)
            if not re.fullmatch(r"[a-z][a-zA-Z0-9]*", field) or field in names:
                raise ValueError(f"Invalid or duplicate Dart identifier: {field}")
            names.add(field)
            css_value, dart_value = project(token)
            css.append(f"  --on-{group}-{name}: {css_value};")
            declaration = f"  static const {field} = {dart_value};"
            if token["$type"] == "fontFamily" and len(declaration) > 80:
                dart.append(f"  static const {field} = <String>[")
                dart.extend(f"    {family.strip()!r}," for family in token["$value"].split(","))
                dart.append("  ];")
            else:
                dart.append(declaration)
        dart.extend(["}", ""])
    css.extend(["}", ""])
    return {
        "tokens/tokens.css": "\n".join(css),
        "packages/flutter/lib/src/tokens.dart": "\n".join(dart),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Reject generated file drift without writing")
    args = parser.parse_args()
    try:
        generated = render(json.loads((ROOT / "tokens/tokens.json").read_text()))
    except (KeyError, TypeError, ValueError) as error:
        parser.exit(1, f"Invalid design tokens: {error}\n")
    stale = []
    for relative, content in generated.items():
        path = ROOT / relative
        if args.check:
            if not path.exists() or path.read_text() != content:
                stale.append(relative)
        else:
            path.write_text(content)
    if stale:
        parser.exit(1, "Generated tokens differ; run just tokens:\n" + "\n".join(stale) + "\n")
    print("Token projections are current." if args.check else "Generated CSS and Flutter tokens.")


if __name__ == "__main__":
    main()

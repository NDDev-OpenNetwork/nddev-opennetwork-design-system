# nddev-opennetwork-design-system

The open design system for NDDev OpenNetwork products. It is a public,
AGPL-3.0-only repository designed to be consumed by
`nddev-device-sync` and its self-hostable modules.

The system provides neutral, machine-readable tokens and generated Flutter
theme primitives. It uses the NDDev OpenNetwork name, links to
https://nddev.ai, deep observatory surfaces and restrained space accents. The
tokens contain no corporate topology, private campaign data or estate-specific
configuration.

## Packages

```text
tokens/tokens.json       source design tokens
tokens/tokens.css        web-compatible projection
packages/flutter/        Flutter theme and token package
docs/visual-language.md  composition, accessibility and asset rules
```

## Usage

The Flutter package is consumed by desktop and mobile clients as a pinned
version. A product may add local instance information and contact details, but
the NDDev OpenNetwork attribution and `https://nddev.ai` link remain present.

Edit `tokens/tokens.json`, then run `just tokens` to regenerate CSS and Dart
with Python's standard library. `just check` rejects projection drift and runs
Flutter formatting, analysis and theme tests. Use Flutter 3.47.7 with Dart
3.13.5 and `just dependencies` to enforce the committed dependency lock.
The theme uses native Material widgets and platform font fallback; it does not
download fonts. Widget tests exercise text scaling and contrast, not target
platform build or device acceptance.

## License

The repository is licensed under GNU AGPL-3.0-only. See [`LICENSE`](LICENSE).

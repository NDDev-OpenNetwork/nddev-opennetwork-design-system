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

## License

The repository is licensed under GNU AGPL-3.0-only. See [`LICENSE`](LICENSE).


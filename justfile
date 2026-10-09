set shell := ["bash", "-euo", "pipefail", "-c"]

default:
    @just --list

tokens:
    python3 tools/generate_tokens.py

tokens-check:
    python3 tools/generate_tokens.py --check
    python3 -B -m unittest discover -s tools

dependencies:
    cd packages/flutter && flutter pub get --enforce-lockfile

format:
    dart format packages/flutter/lib packages/flutter/test

fmt-check:
    dart format --output=none --set-exit-if-changed packages/flutter/lib packages/flutter/test

analyze:
    cd packages/flutter && flutter analyze

test:
    cd packages/flutter && flutter test

check: tokens-check fmt-check analyze test

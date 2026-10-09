set shell := ["bash", "-euo", "pipefail", "-c"]

default:
    @just --list

format:
    dart format packages/flutter/lib packages/flutter/test

fmt-check:
    dart format --output=none --set-exit-if-changed packages/flutter/lib packages/flutter/test

analyze:
    cd packages/flutter && flutter analyze

test:
    cd packages/flutter && flutter test

check: fmt-check analyze test

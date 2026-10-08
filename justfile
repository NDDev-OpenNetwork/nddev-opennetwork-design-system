set shell := ["bash", "-euo", "pipefail", "-c"]

default:
    @just --list

format:
    dart format packages/flutter/lib packages/flutter/test

analyze:
    flutter analyze packages/flutter

test:
    flutter test packages/flutter/test

check: analyze test


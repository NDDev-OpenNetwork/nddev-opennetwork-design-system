#!/usr/bin/env bash
# Linux Pillow wheels use the host zlib. Scope the canonical backend to one check.
set -euo pipefail
test "$(uname -s)-$(uname -m)" = Linux-x86_64
test "$#" -gt 0
renderer_dir=$(mktemp -d)
trap 'rm -rf -- "$renderer_dir"' EXIT
curl --fail --silent --show-error --location --retry 2 --max-time 60 \
  --max-filesize 2097152 https://zlib.net/fossils/zlib-1.3.1.tar.gz \
  --output "$renderer_dir/source.tar.gz"
echo "9a93b2b7dfdac77ceba5a558a580e74667dd6fede4585b91eefb60f03b72df23  $renderer_dir/source.tar.gz" | sha256sum --check -
tar -xf "$renderer_dir/source.tar.gz" -C "$renderer_dir"
if ! (
  cd "$renderer_dir/zlib-1.3.1"
  timeout 60 ./configure --prefix="$renderer_dir/prefix"
  timeout 120 make -j4
  timeout 60 make check
  timeout 60 make install
) >"$renderer_dir/build.log" 2>&1; then
  cat "$renderer_dir/build.log"
  exit 1
fi
LD_LIBRARY_PATH="$renderer_dir/prefix/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" "$@"

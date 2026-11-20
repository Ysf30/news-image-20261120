#!/usr/bin/env python3
"""Entry program for news-image-20261120.

Copies the front-page image this repository holds (entry.png) to
/output/entry.png, byte for byte. The image sums up Friday
20 November 2026 world news: Cyclone Akvan, the Shenzhen trilateral
aftermath, the ICJ Myanmar judgment, and 30+ more stories.
Runs offline, deterministically, with only the standard library.
"""

import hashlib
import os
import shutil
import struct
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(src, "rb") as fh:
        digest = hashlib.sha256(fh.read()).hexdigest()
    shutil.copyfile(src, dst)
    with open(dst, "rb") as fh:
        data = fh.read()
    if hashlib.sha256(data).hexdigest() != digest:
        print("copy mismatch", file=sys.stderr)
        return 1
    # Gate check: whole PNG, 1024x1024 at most, under 1 MiB.
    if data[:8] != b"\x89PNG\r\n\x1a\n" or len(data) > 1048576:
        print("not a valid PNG under 1 MiB", file=sys.stderr)
        return 1
    width, height = struct.unpack(">II", data[16:24])
    if width > 1024 or height > 1024:
        print("image larger than 1024x1024", file=sys.stderr)
        return 1
    print(f"entry.png -> {dst} ({len(data)} bytes, {width}x{height}, "
          f"sha256 {digest[:16]}...)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

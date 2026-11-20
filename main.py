#!/usr/bin/env python3
"""news-image-20261120 — entry point.

The picture for Friday 20 November 2026, "THE WORLD IN ONE PAGE",
is stored next to this file as entry.png (drawn fresh in this
session by build_image.py: Cyclone Akvan's landfall, the Trump-Xi-
Putin peace declaration from Shenzhen, the ICJ's 9-6 genocide
ruling on Myanmar, and 27 more stories from the day).

This program does one thing: copy that PNG to the output folder
unchanged. Standard library only, no network, no randomness, no
arguments — two runs write byte-identical files.

Usage:
    MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import hashlib
import os
import sys
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "entry.png"
LIMIT_BYTES = 1_048_576
LIMIT_SIDE = 1024
SIGNATURE = b"\x89PNG\r\n\x1a\n"


def read_and_check():
    data = SOURCE.read_bytes()
    if data[:8] != SIGNATURE:
        raise SystemExit("entry.png: bad PNG signature")
    if data[12:16] != b"IHDR":
        raise SystemExit("entry.png: missing IHDR chunk")
    if len(data) > LIMIT_BYTES:
        raise SystemExit("entry.png: over the 1 MiB limit")
    if len(data) < 12 or data[-8:-4] != b"IEND":
        raise SystemExit("entry.png: missing IEND trailer")
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    if width > LIMIT_SIDE or height > LIMIT_SIDE:
        raise SystemExit("entry.png: over the 1024x1024 limit")
    return data, width, height


def main():
    data, width, height = read_and_check()
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    target.write_bytes(data)
    written = target.read_bytes()
    if hashlib.sha256(written).hexdigest() != hashlib.sha256(data).hexdigest():
        print("error: output does not match entry.png", file=sys.stderr)
        return 1
    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {target} — {len(data)} bytes, {width}x{height}, "
          f"sha256 {digest[:16]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

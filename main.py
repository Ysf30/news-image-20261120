#!/usr/bin/env python3
"""news-image-20261120 entrypoint.

Reads the front-page PNG stored next to this file and writes it out
unchanged to the output folder. The picture sums up Friday
20 November 2026: Cyclone Akvan's landfall in India, the
Trump-Xi-Putin Peace Declaration from Shenzhen, the ICJ ruling
that Myanmar committed genocide against the Rohingya, and
28 more stories from the day.

Pure standard library, no network, no randomness: two runs
produce byte-identical output.
"""
import os
import sys
from hashlib import sha256
from pathlib import Path

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576
MAX_SIDE = 1024


def load_image():
    here = Path(__file__).resolve().parent
    blob = (here / "entry.png").read_bytes()
    return blob


def check_blob(blob):
    if len(blob) < 24:
        raise ValueError("entry.png is too short to be a PNG file")
    if blob[:8] != PNG_MAGIC:
        raise ValueError("entry.png is not a PNG file")
    if blob[12:16] != b"IHDR":
        raise ValueError("entry.png has no IHDR chunk")
    if len(blob) > MAX_BYTES:
        raise ValueError("entry.png is over the 1 MiB limit")
    wide = int.from_bytes(blob[16:20], "big")
    tall = int.from_bytes(blob[20:24], "big")
    if wide > MAX_SIDE or tall > MAX_SIDE:
        raise ValueError("entry.png is larger than 1024x1024")
    return wide, tall


def run():
    blob = load_image()
    wide, tall = check_blob(blob)
    target = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    target.mkdir(parents=True, exist_ok=True)
    dest = target / "entry.png"
    dest.write_bytes(blob)
    again = dest.read_bytes()
    if sha256(again).hexdigest() != sha256(blob).hexdigest():
        print("output bytes differ from source", file=sys.stderr)
        return 1
    print(f"wrote {dest} ({len(blob)} bytes, {wide}x{tall}, "
          f"sha256 {sha256(blob).hexdigest()[:12]})")
    return 0


if __name__ == "__main__":
    sys.exit(run())

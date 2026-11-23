#!/usr/bin/env python3
"""news-22 b6 map-timeline: copy the entry image to the output directory.

The image (entry.png, 1024x1024, 207570 bytes) is drawn by draw.py in the
build directory; this program only copies it, verifies the copy, and exits.
Standard library only, no network.
"""
import hashlib
import os
import shutil
import sys

EXPECTED_SHA256 = "b8824eaa40cac8183dc6c56ea01e4ca08e103f73554b3ef365f058462287c431"
EXPECTED_SIZE = 207570


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    # Re-read the copy and verify it byte for byte: PNG magic, size, sha256.
    with open(dst, "rb") as fh:
        data = fh.read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        print("not a PNG file", file=sys.stderr)
        return 1
    if len(data) != EXPECTED_SIZE:
        print(f"size mismatch: {len(data)} != {EXPECTED_SIZE}", file=sys.stderr)
        return 1
    if hashlib.sha256(data).hexdigest() != EXPECTED_SHA256:
        print("sha256 mismatch", file=sys.stderr)
        return 1
    print(f"wrote {dst} ({len(data)} bytes, sha256 {EXPECTED_SHA256[:16]}...)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

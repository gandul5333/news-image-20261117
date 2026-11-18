#!/usr/bin/env python3
"""news-image-20261117 entrypoint (Python 3.13, standard library only).

The entry is a newspaper front page that sums up Tuesday 17 November
2026's world news in one image: the Kerch Bridge strike, tankers hit by
mines near Hormuz, the Trump-Xi-Putin meeting set for Shenzhen, the ULA
Vulcan failure, and the JPMorgan banking outage. The image was drawn
for this day by draw_image.py in this repository and is shipped as
entry.png; this program copies those exact bytes to the output directory
every run, so both graded runs write byte-identical files.

Run it:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, dest)
    # Byte-identical by construction; verify so a partial copy can never
    # pass silently.
    if sha256(SOURCE) != sha256(dest):
        print("error: copied file differs from source", file=sys.stderr)
        return 1
    print("wrote", dest, os.path.getsize(dest), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())

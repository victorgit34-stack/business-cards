#!/usr/bin/env python3
"""Set a line of text in Inter as an SVG <path> (outlined text, no font needed to display/print).

    python3 text2path.py "Jane Smith" --weight regular --size 10 --x 18 --y 70
    python3 text2path.py "City, ST 00000" --weight light --size 6.4 --anchor end --x 234 --y 126 --fill "#E3E4E6"

--x/--y is the start (or end with --anchor end) of the text on its BASELINE, in the card's
252 x 144 coordinate space. --tracking is extra space between letters in points.
Prints one <path .../> element to paste into card-front.svg / card-back.svg in place of the old one.
Needs: pip install fonttools
"""
import argparse, os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = {"light": "fonts/Inter-Light.ttf", "regular": "fonts/Inter-Regular.ttf"}


def text_path(text, weight="regular", size=10.0, tracking=0.0, x=0.0, y=0.0, anchor="start"):
    font = TTFont(os.path.join(HERE, FONTS[weight]))
    gs, cmap, hmtx = font.getGlyphSet(), font.getBestCmap(), font["hmtx"]
    k = size / font["head"].unitsPerEm
    names = [cmap.get(ord(c), ".notdef") for c in text]
    advance = sum(hmtx[n][0] * k for n in names) + tracking * (len(names) - 1)
    pen_x = x - advance if anchor == "end" else x - advance / 2 if anchor == "middle" else x
    pen = SVGPathPen(gs, ntos=lambda v: f"{v:.3f}".rstrip("0").rstrip("."))
    for n in names:
        gs[n].draw(TransformPen(pen, (k, 0, 0, -k, pen_x, y)))  # flip y: font units are y-up
        pen_x += hmtx[n][0] * k + tracking
    return pen.getCommands(), advance


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("text")
    ap.add_argument("--weight", choices=FONTS, default="regular")
    ap.add_argument("--size", type=float, default=10)
    ap.add_argument("--tracking", type=float, default=0)
    ap.add_argument("--x", type=float, default=18)
    ap.add_argument("--y", type=float, default=72)
    ap.add_argument("--anchor", choices=["start", "middle", "end"], default="start")
    ap.add_argument("--fill", default="#FFFFFF")
    a = ap.parse_args()
    d, w = text_path(a.text, a.weight, a.size, a.tracking, a.x, a.y, a.anchor)
    print(f'<path fill="{a.fill}" d="{d}"/>')
    print(f"<!-- width {w:.2f} pt -->", flush=True)

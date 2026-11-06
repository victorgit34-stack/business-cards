#!/usr/bin/env python3
"""Rebuild every output for this card from the two master files.

Masters (edit only these):  card-front.svg, card-back.svg   (252 x 144 viewBox = 3.5 x 2 in trim)

Outputs:
  card-front-print.svg, card-back-print.svg   3.75 x 2.25 in (1/8 in bleed)
  card-preview.svg, card-preview.png          both sides side by side on a grey sheet
  greystone-business-card-print.pdf           2 pages, 1/8 in bleed (most printers)
  greystone-business-card-vistaprint.pdf      2 pages, 3.62 x 2.12 in (Vistaprint full-bleed size)

Usage:  python3 build.py
Needs:  rsvg-convert (brew install librsvg)  OR  pip install cairosvg pypdf
"""
import os, re, shutil, subprocess, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)


def inner(path):
    s = open(path, encoding="utf-8").read()
    m = re.match(r"\s*<svg[^>]*>(.*)</svg>\s*$", s, re.S)
    if not m:
        raise SystemExit(f"{path}: expected a single root <svg>")
    return m.group(1)


def write(path, s):
    open(path, "w", encoding="utf-8").write(s)


def bleed_svg(body, bleed_pt):
    """Wrap a 252x144 card in a page that extends bleed_pt past the trim on every side.
    Backgrounds in the masters already run 9 pt past the trim, so any bleed up to 9 pt works."""
    w, h = 252 + 2 * bleed_pt, 144 + 2 * bleed_pt
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}" '
            f'width="{w:g}pt" height="{h:g}pt"><g transform="translate({bleed_pt:g},{bleed_pt:g})">'
            f"{body}</g></svg>")


def preview_svg(front, back):
    card = lambda x, b: (f'<svg x="{x}" y="20" width="252" height="144" viewBox="0 0 252 144" '
                         f'overflow="hidden">{b}</svg><rect x="{x}" y="20" width="252" height="144" '
                         f'fill="none" stroke="#D6D6D2" stroke-width="0.5"/>')
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 584 184" width="2336" height="736">'
            '<rect width="584" height="184" fill="#EEEEEB"/>' + card(28, front) + card(304, back) + "</svg>")


def render_png(svg, png, w, h):
    if shutil.which("rsvg-convert"):
        subprocess.run(["rsvg-convert", "-w", str(w), "-h", str(h), svg, "-o", png], check=True)
    else:
        import cairosvg
        cairosvg.svg2png(url=svg, write_to=png, output_width=w, output_height=h)


def render_pdf(svgs, pdf):
    if shutil.which("rsvg-convert"):  # rsvg-convert writes one page per input file
        subprocess.run(["rsvg-convert", "-f", "pdf", *svgs, "-o", pdf], check=True)
        return
    import cairosvg
    from pypdf import PdfWriter
    out = PdfWriter()
    with tempfile.TemporaryDirectory() as tmp:
        for i, s in enumerate(svgs):
            p = os.path.join(tmp, f"{i}.pdf")
            cairosvg.svg2pdf(url=s, write_to=p)
            out.append(p)
        out.write(pdf)


front, back = inner("card-front.svg"), inner("card-back.svg")

write("card-front-print.svg", bleed_svg(front, 9))
write("card-back-print.svg", bleed_svg(back, 9))
write("card-preview.svg", preview_svg(front, back))
render_png("card-preview.svg", "card-preview.png", 2336, 736)
render_pdf(["card-front-print.svg", "card-back-print.svg"], "greystone-business-card-print.pdf")

VP = 0.06 * 72  # Vistaprint: 3.62 x 2.12 in full bleed -> 0.06 in each side
with tempfile.TemporaryDirectory() as tmp:
    f, b = os.path.join(tmp, "f.svg"), os.path.join(tmp, "b.svg")
    write(f, bleed_svg(front, VP))
    write(b, bleed_svg(back, VP))
    render_pdf([f, b], "greystone-business-card-vistaprint.pdf")

print("built: print SVGs, preview SVG/PNG, print PDF, Vistaprint PDF")

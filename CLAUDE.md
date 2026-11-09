# Greystone Consulting Group — business card (design #7, black/red)

Two-sided US business card. Front: black with the centred logo. Back (info side): red with the logo top-left, name, title and contact details.
The user designs dark panels by preference: black backgrounds with red, grey and white for text and highlights.

## Files

| File | What it is |
|---|---|
| `card-front.svg`, `card-back.svg` | **Masters. Edit only these.** 252 × 144 viewBox = 3.5 × 2 in trim (1 unit = 1 pt). Backgrounds run 9 pt past the trim on every side for bleed. |
| `build.py` | Regenerates every file below from the masters. Run `python3 build.py` after any edit. |
| `text2path.py` | Sets new text in Inter as an outlined `<path>` (see "Changing text"). |
| `fonts/` | Inter Light + Regular, the brand fonts (SIL Open Font License). |
| `card-front-print.svg`, `card-back-print.svg` | Generated. 3.75 × 2.25 in, ⅛ in bleed. |
| `card-preview.svg` / `.png` | Generated. Both sides side by side on a light grey sheet. Look at the PNG to check your work. |
| `greystone-business-card-print.pdf` | Generated. 2 pages (front, back), ⅛ in bleed, for most printers. |
| `greystone-business-card-vistaprint.pdf` | Generated. 2 pages at Vistaprint's full-bleed size, 3.62 × 2.12 in. Upload this one to Vistaprint. |

`build.py` needs `rsvg-convert` (`brew install librsvg`) or `pip install cairosvg pypdf`. `text2path.py` needs `pip install fonttools`.

## Important: all text is outlined

No `<text>` elements. Every line is a single `<path>` of glyph outlines, so the files display and print identically anywhere with no fonts installed. This also means:
- Text cannot be edited by changing a string. Regenerate the line with `text2path.py` and swap the whole `<path>`.
- Vistaprint cannot edit text in an uploaded design. Every change has to be made here and re-uploaded.

## Colours

| Hex | Use |
|---|---|
| `#1C1D1F` | Black: front background, bottom row of the logo on the back |
| `#B3262E` | Red: back background, bottom row of the logo on the front |
| `#E3E4E6` | Light grey: logo top row, title, address, CONSULTING GROUP on the back |
| `#8C8F93` | Mid grey: logo middle row, CONSULTING GROUP on the front |
| `#FFFFFF` | White: GREYSTONE, name, phone, email, website, divider |

## Logo

The mark is three courses of stone: two bricks on top, half / whole / half in the middle, two bricks on the bottom. Colours top to bottom: light grey, mid grey, then red on the black front and black (`#1C1D1F`) on the red back, so the bottom row always contrasts with the background.

## Layout of `card-back.svg` (in document order)

1. Background `<rect>` `#B3262E`.
2. `<g transform="translate(18 18) scale(1.4) translate(-18 -18)">`: the logo block, enlarged 40% from its top-left corner (18,18). It contains the 7 logo `<rect>`s, the GREYSTONE path, and the CONSULTING GROUP path. CONSULTING GROUP is the front's tagline path reused with its own `transform` (scaled ×0.6932, shifted 3 pt right of GREYSTONE). On the card the block spans about x 18–158, y 18–49. Change its size by changing `scale(1.4)`.
3. Text lines, one `<path>` each, all outside the group:

| Line | Font | Size | Tracking | Position (baseline) | Fill |
|---|---|---|---|---|---|
| Jordan Avery | Inter Regular | 11 | 0.3 | x 18, y 70 | `#FFFFFF` |
| MANAGING PARTNER | Inter Light | 6.5 | 1.4 | x 18, y 82 | `#E3E4E6` |
| divider | `<rect x="18" y="93" width="24" height="0.8">` | | | | `#FFFFFF` |
| +1 (555) 010-0142 | Inter Regular | 7 | 0.2 | x 18, y 106 | `#FFFFFF` |
| jordan.avery@yourdomain.com | Inter Regular | 7 | 0.2 | x 18, y 116 | `#FFFFFF` |
| yourdomain.com | Inter Regular | 7 | 0.2 | x 18, y 126 | `#FFFFFF` |
| 123 Main Street, Suite 400 | Inter Light | 6.5 | 0.2 | right-aligned to x 234, y 116 | `#E3E4E6` |
| City, ST 00000 | Inter Light | 6.5 | 0.2 | right-aligned to x 234, y 126 | `#E3E4E6` |

Every value except the name/phone/email/web/address text is a placeholder; the user's real details haven't been filled in yet.

## Layout of `card-front.svg`

Background `#1C1D1F`, then the 7 logo rects (x 51–93.4, y 50.8–93.2), then GREYSTONE (Inter Light 12.13, tracking 3.03, x 103.75, baseline 71.39, white), then CONSULTING GROUP (Inter Regular 5.82, tracking 2.44, x 103.75, baseline 82.31, `#8C8F93`).

## Changing text

```
python3 text2path.py "Jane Smith" --weight regular --size 11 --tracking 0.3 --x 18 --y 70
python3 text2path.py "Austin, TX 78701" --weight light --size 6.5 --tracking 0.2 --anchor end --x 234 --y 126 --fill "#E3E4E6"
```
Each command prints a `<path …/>`. Replace the matching line's `<path>` in the master, keeping the same position in the file, then run `build.py`. Find the old path by its fill and the y range of its coordinates.

`text2path.py` also prints the line's width. Long email addresses can run into the right-aligned address: keep the left column ending before about x 140 and the address starting after about x 145. If they collide, shrink the size slightly or move the address under the website.

## Print specs

- Trim 3.5 × 2 in. Keep text and logos at least 0.125 in (9 pt) inside the trim. Everything currently sits 18 pt in.
- Vistaprint: full bleed 3.62 × 2.12 in, trim 3.5 × 2 in, safe area 3.38 × 1.88 in. Use `greystone-business-card-vistaprint.pdf`.
- Other printers usually want ⅛ in bleed (3.75 × 2.25 in): `greystone-business-card-print.pdf`.

## History

Based on `business-cards/red-black-grey/04-black-red` (#7 of 9 designs in the Greystone folder; that original is unchanged). Changes made in this version:
1. Back logo recoloured to match the front: light grey, mid grey, red, with the red bricks outlined.
2. CONSULTING GROUP added under GREYSTONE on the back, slightly right.
3. Back logo block enlarged 40%.
4. Bottom logo bricks on the red back changed from outlined red to solid black.

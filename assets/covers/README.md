# Cover page artwork and typeface (PDF Studio v2.3.0)

Everything the **Cover** button needs to draw the Big M cover — the cover the
Science and Maths portals print — as a page of the PDF. The drawing code is
section 20 of `index.html` (search `COVER PAGES`).

| File | What it is | Where it came from |
| --- | --- | --- |
| `science-icons-v2.png` | 1254 × 1254 RGBA sheet of 16 pixel-art science icons in a 4 × 4 grid | `polymathlc/cer` `assets/worksheet-covers/science-icons-v2.png`, byte for byte |
| `math-pixel-icons.png` | 672 × 672 RGBA sheet of 16 pixel-art maths symbols, 168 px cells | `polymathlc/math` `assets/worksheet-covers/math-pixel-icons.png`, byte for byte |
| `polymath-learning-centre.png` | The Polymath Learning Centre logo, 2681 × 1957 | `polymathlc/cer` `assets/branding/polymath-learning-centre.png`, byte for byte |
| `fonts/polymath-cover-gothic-regular.ttf` | The cover typeface, regular | Built from TeX Gyre Adventor 2.501 by `tools/cover-font-otf2ttf.py` |
| `fonts/polymath-cover-gothic-bold.ttf` | The cover typeface, bold | Built from TeX Gyre Adventor 2.501 by `tools/cover-font-otf2ttf.py` |
| `fonts/GUST-FONT-LICENSE.txt` | The typeface's licence | TeX Gyre distribution |

## The icon sheets

Science grid, left to right, top to bottom: atom, test tubes, flask,
microscope / DNA, seedling, magnet, thermometer / light bulb, planet, gear,
water drop / battery, beaker, magnifying glass, leaf. The sheet was generated
with slightly uneven gutters, so it is cropped at the inspected transparent
seams (`COVER_SUBJECTS.science.atlas` — the same numbers as `atlasCells.science`
in the portal).

Maths grid: plus, minus, times, divide / equals, percent, pi, square root /
fraction pie, protractor, infinity, not-equal / less-than, greater-than,
set square, cube. Clean 168 px cells, drawn without smoothing and only ever
scaled by whole numbers, so the pixels stay square on paper.

Which cell sits in each of the 31 places is the portals' own choice:
`M_ICONS` (Science) and `M_CELLS` (Maths) in their `worksheet-cover.js`,
copied as `COVER_ICON_PLACES` and `COVER_MATH_CELLS`.

On a drawn cover the Science cells are reduced to 240 px and their colours
rounded to 32 levels per channel (`COVER_POSTERISE_*`), which takes a cover
from about 1.4 MB to about 380 KB with no difference you can see at the icons'
38% strength. The files here are untouched; the reduction happens at drawing
time.

## The typeface

The portals set the cover in **Century Gothic**, which matches ITC Avant
Garde's metrics. **TeX Gyre Adventor** is a free Avant Garde, so it sets the
same words to the same widths and breaks titles in the same places.

Adventor ships as CFF OpenType, and pdf-lib's subsetter (through
`@pdf-lib/fontkit` 1.1.1) produces broken fonts from CFF outlines. TrueType
outlines subset cleanly, so `tools/cover-font-otf2ttf.py` converts the outlines
(within one font unit), keeps the character map, metrics and kerning, pads every
glyph to an even length (fontkit's short `loca` tables need it), and — as the
GUST Font License asks of a changed font — renames the family **Polymath
Cover Gothic**, crediting Adventor in the font's Description record. Only the
glyphs a cover actually uses are embedded in a PDF: a few kilobytes.

TeX Gyre Adventor is © 2007–2018 B. Jackowski, J. M. Nowacki et al. on behalf
of TeX Users Groups, distributed under the GUST Font License (an instance of
the LaTeX Project Public License); see `fonts/GUST-FONT-LICENSE.txt`.

## When a file cannot be reached

The page first reads these files from beside itself. If that fails (for
example when `index.html` is opened straight from disk), the same paths are
tried on `raw.githubusercontent.com/polymathlc/pdf/main/assets/covers/`, and the
icon sheets and logo are also tried in the cer and math repositories. A cover
that still cannot get a piece is drawn without it — Helvetica for the type, no
icons, an empty logo space — and the dialog says which.

## Replacing a file

Keep the sizes, the grids and the transparency. A replacement icon sheet drawn
at a different pixel size still crops correctly (the grid is scaled to the real
sheet), but the cells must stay in the same order. After any change, add a
cover of each subject and compare it with the portals' own.

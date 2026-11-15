"""Build the cover page's typeface, "Polymath Cover Gothic", from TeX Gyre Adventor.

WHY THIS EXISTS
    The Polymath portals set their Big M cover in Century Gothic. Century Gothic
    was drawn to share ITC Avant Garde's metrics, and TeX Gyre Adventor is a free
    Avant Garde (GUST Font License), so it sets the same words to the same widths.

    Adventor ships as CFF OpenType (.otf), and pdf-lib's subsetter (via
    @pdf-lib/fontkit 1.1.1) writes broken fonts when it subsets CFF outlines.
    TrueType outlines subset cleanly, so this script converts the outlines and
    keeps everything else (cmap, metrics, kerning in GPOS/kern) untouched.

    The GUST Font License asks that a changed font be renamed, so the result is
    called "Polymath Cover Gothic", and its Description name record credits the
    original. GUST-FONT-LICENSE.txt sits beside the fonts in assets/covers/fonts.

USAGE
    pip install fonttools
    # texgyreadventor-regular.otf / -bold.otf come from the TeX Gyre release
    # (gust.org.pl/projects/e-foundry/tex-gyre/adventor, or Debian/Ubuntu's
    # fonts-texgyre package: /usr/share/texmf/fonts/opentype/public/tex-gyre/).
    python3 tools/cover-font-otf2ttf.py texgyreadventor-regular.otf \
        assets/covers/fonts/polymath-cover-gothic-regular.ttf Regular
    python3 tools/cover-font-otf2ttf.py texgyreadventor-bold.otf \
        assets/covers/fonts/polymath-cover-gothic-bold.ttf Bold
"""
import sys

from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont, newTable

FAMILY = "Polymath Cover Gothic"
CREDIT = ("Derived from TeX Gyre Adventor 2.501, (c) 2007-2018 B. Jackowski, "
          "J. M. Nowacki et al. on behalf of TeX Users Groups, under the GUST Font "
          "License. Outlines converted to TrueType and the family renamed, as that "
          "licence requests of a changed font.")

# Cubic-to-quadratic tolerance in font units (1000 per em): invisible in print.
CURVE_TOLERANCE = 1.0


def convert(source_path, target_path, style):
    font = TTFont(source_path)
    glyph_order = font.getGlyphOrder()
    glyph_set = font.getGlyphSet()

    glyf = newTable("glyf")
    glyf.glyphOrder = glyph_order
    glyf.glyphs = {}
    # fontkit writes a subset with a SHORT loca table whenever it is small,
    # and a short loca stores every offset halved, so every glyph must be an
    # even number of bytes long. Unpadded glyphs make the subset lose letters.
    glyf.padding = 4
    for glyph_name in glyph_order:
        pen = TTGlyphPen(glyph_set)
        glyph_set[glyph_name].draw(Cu2QuPen(pen, CURVE_TOLERANCE, reverse_direction=True))
        glyf.glyphs[glyph_name] = pen.glyph()

    font["loca"] = newTable("loca")
    font["glyf"] = glyf
    del font["CFF "]
    if "VORG" in font:
        del font["VORG"]

    maxp = font["maxp"]
    maxp.tableVersion = 0x00010000
    for attribute in ("maxZones", "maxTwilightPoints", "maxStorage", "maxFunctionDefs",
                      "maxInstructionDefs", "maxStackElements", "maxSizeOfInstructions",
                      "maxComponentElements", "maxPoints", "maxContours",
                      "maxCompositePoints", "maxCompositeContours", "maxComponentDepth"):
        setattr(maxp, attribute, 1 if attribute == "maxZones" else 0)

    # The loca format (short or long) is left for fontTools to choose on save.
    font["head"].glyphDataFormat = 0
    post = font["post"]
    post.formatType = 2.0
    post.extraNames = []
    post.mapping = {}
    post.glyphOrder = glyph_order
    font.sfntVersion = "\x00\x01\x00\x00"

    postscript_name = "PolymathCoverGothic-" + style
    full_name = FAMILY if style == "Regular" else FAMILY + " " + style
    names = font["name"]
    for record in list(names.names):
        if record.nameID in (1, 3, 4, 6, 10, 16, 17, 21, 22):
            names.removeNames(nameID=record.nameID)
    for name_id, value in ((1, FAMILY), (2, style), (3, postscript_name + ";2.501"),
                           (4, full_name), (6, postscript_name), (10, CREDIT),
                           (16, FAMILY), (17, style)):
        names.setName(value, name_id, 3, 1, 0x409)
        names.setName(value, name_id, 1, 0, 0)

    font.recalcBBoxes = True
    glyf.compile(font)
    font.save(target_path)
    print(target_path, "-", len(glyph_order), "glyphs")


if __name__ == "__main__":
    if len(sys.argv) != 4 or sys.argv[3] not in ("Regular", "Bold"):
        sys.exit(__doc__)
    convert(sys.argv[1], sys.argv[2], sys.argv[3])

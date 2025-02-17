import math
from emicText import EmicText
from glyphDictionary import SingleSVGGlyphDictionary
from relLine import RelLine
import relaxer

dictionary = SingleSVGGlyphDictionary('unlws_glyphs/glyphs.svg')

def main(canvas, append_text):
    text = EmicText()
    
    firstsg = dictionary.glyph_by_id("I")
    firstsg = relaxer.DifferentialGlyph.from_glyph(firstsg)
    firstsg.x = -2.
    firstsg.y = 0.
    firstsg.angle = math.pi/6#-math.pi/2
    text.add_glyph(firstsg)

    cat = dictionary.glyph_by_id("cat")
    cat = relaxer.DifferentialGlyph.from_glyph(cat)
    cat.x = 2.
    cat.y = 0.
    cat.angle = math.pi
    text.add_glyph(cat)

    rel = RelLine(firstsg, "X", cat, "X")
    text.add_rel(rel)

    canvas.render(text)

    append_text(f"Max curvature: {str(relaxer.curvature_penalty(rel))}. ")
    firstsg.dangle = 1.
    append_text(f"Derivative: {str(relaxer.deriv_curvature_penalty(rel))}. ")

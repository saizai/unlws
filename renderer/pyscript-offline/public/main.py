import math
from pyscript import document
from canvas import HTMLDOMCanvas
from emicText import EmicText
from glyphDictionary import SingleSVGGlyphDictionary
from relLine import RelLine
import relaxer

board = document.querySelector("#svgboard")
canvas = HTMLDOMCanvas(board)
text = EmicText()

dictionary = SingleSVGGlyphDictionary('unlws_glyphs/glyphs.svg')

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

document.body.append(f"Max curvature: {str(relaxer.curvature_penalty(rel))}. ")
firstsg.dangle = 1.
document.body.append(f"Derivative: {str(relaxer.deriv_curvature_penalty(rel))}. ")

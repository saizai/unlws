import math
from pyscript import document
from canvas import HTMLDOMCanvas
from emicText import EmicText
from glyphDictionary import SingleSVGGlyphDictionary
from relLine import RelLine
import relaxer

board = document.querySelector("#svgboard")
canvas = HTMLDOMCanvas(board)

dictionary = SingleSVGGlyphDictionary('unlws_glyphs/glyphs.svg')

def make_test_text(y_offset=0, I_angle_offset=0, distance_multiplier = 1):
    text = EmicText()
    
    firstsg = dictionary.glyph_by_id("I")
    firstsg = relaxer.DifferentialGlyph.from_glyph(firstsg)
    firstsg.x = -2. * distance_multiplier
    firstsg.y = 0. + y_offset
    firstsg.angle = -math.pi/2 + I_angle_offset#math.pi/6#-math.pi/2
    text.add_glyph(firstsg)

    cat = dictionary.glyph_by_id("cat")
    cat = relaxer.DifferentialGlyph.from_glyph(cat)
    cat.x = 2. * distance_multiplier
    cat.y = 0. + y_offset
    cat.angle = math.pi
    text.add_glyph(cat)

    rel = RelLine(firstsg, "X", cat, "X")
    text.add_rel(rel)


    cat2 = dictionary.glyph_by_id("cat")
    cat2 = relaxer.DifferentialGlyph.from_glyph(cat2)
    cat2.x = 2. * distance_multiplier
    cat2.y = 1. + y_offset
    cat2.angle = math.pi
    text.add_glyph(cat2)

    rel2 = RelLine(firstsg, "X", cat2, "X")
    text.add_rel(rel2)
    
    cat.dx = 1.
    cat2.dx = 1.
    
    return text

text = make_test_text(0, math.pi/6)
# text2 = make_test_text(2, math.pi/6)
text2 = make_test_text(5, math.pi/6)
relaxer.relax(text2)

canvas.render(text)
canvas.render(text2)

# text3 = make_test_text(8, math.pi/6, 2)
# # text4 = make_test_text(2, math.pi/6)
# text4 = make_test_text(11, math.pi/6, 2)
# relaxer.relax(text4)

# canvas.render(text3)
# canvas.render(text4)


document.body.append(f"t1: ")
document.body.append(f"Non-constant-velocity penalty: {str(relaxer.velocity_penalty(text.rels[0]))}. ")
document.body.append(f"Derivative: {str(relaxer.deriv_velocity_penalty(text.rels[0]))}. ")
document.body.append(f"t2: ")
document.body.append(f"Non-constant-velocity penalty: {str(relaxer.velocity_penalty(text2.rels[0]))}. ")
# cat.dx = 1.
document.body.append(f"Derivative: {str(relaxer.deriv_velocity_penalty(text2.rels[0]))}. ")

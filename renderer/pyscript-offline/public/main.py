import math
from pyscript import document
from canvas import HTMLDOMCanvas
from emicText import EmicText
from glyphDictionary import SingleSVGGlyphDictionary
from relLine import RelLine
import relaxer

board = document.querySelector("#svgboard")

dictionary = SingleSVGGlyphDictionary('unlws_glyphs/glyphs.svg')

def make_test_text(I_angle_offset = 0, distance_multiplier = 1):
    text = EmicText()

    firstsg = dictionary.glyph_by_id("I")
    firstsg = relaxer.DifferentialGlyph.from_glyph(firstsg)
    firstsg.x = -2. * distance_multiplier
    firstsg.y = 0.
    firstsg.angle = -math.pi/2 + I_angle_offset#math.pi/6#-math.pi/2
    text.add_glyph(firstsg)

    cat = dictionary.glyph_by_id("cat")
    cat = relaxer.DifferentialGlyph.from_glyph(cat)
    cat.x = 2. * distance_multiplier
    cat.y = 0.
    cat.angle = math.pi
    text.add_glyph(cat)

    rel = RelLine(firstsg, "X", cat, "X")
    text.add_rel(rel)

    cat2 = dictionary.glyph_by_id("cat")
    cat2 = relaxer.DifferentialGlyph.from_glyph(cat2)
    cat2.x = 2. * distance_multiplier
    cat2.y = 1.
    cat2.angle = math.pi
    text.add_glyph(cat2)

    rel2 = RelLine(firstsg, "X", cat2, "X")
    text.add_rel(rel2)
    
    cat.dx = 1.
    cat2.dx = 1.
    
    return text

def render_with_comments(text, description):
    sub_board = document.createElement('div')
    canvas = HTMLDOMCanvas(sub_board)

    canvas.render(text)

    board.append(sub_board)


    p = document.createElement("p")
    p.innerHTML += f"{description}:<br>"
    # p.innerHTML += f"Non-constant-velocity penalty: {str(relaxer.total_penalty(text, {"velocity": 1, "curvature": 0, "distance": 0}))}.<br>"
    # p.innerHTML += f"Derivative for top rel: {str(relaxer.deriv_velocity_penalty(text.rels[0]))}.<br>"
    p.innerHTML += f"Curvature penalty: {str(relaxer.total_penalty(text, {"velocity": 0, "curvature": 1, "distance": 0}))}.<br>"
    p.innerHTML += f"Curvature squared penalty: {str(relaxer.total_penalty(text, {"velocity": 0, "curvature": 0, "distance": 0, "curvature_squared": 1}))}.<br>"
    p.innerHTML += f"Curvature penalty for top rel: {str(relaxer.curvature_penalty(text.rels[0]))}.<br>"
    p.innerHTML += f"Curvature penalty for bottom rel: {str(relaxer.curvature_penalty(text.rels[1]))}.<br>"

    board.append(p)

text = make_test_text(math.pi/6)
render_with_comments(text, "Initial")

velocity_relaxed_text = make_test_text(math.pi/6)
relaxer.relax(velocity_relaxed_text, penalty_coefficients={"velocity": 1, "curvature": 0})
render_with_comments(velocity_relaxed_text, "Relaxed velocity")

curvature_relaxed_text = make_test_text(math.pi/6)
relaxer.relax(curvature_relaxed_text, penalty_coefficients={"velocity": 0, "curvature": 5})
render_with_comments(curvature_relaxed_text, "Relaxed max curvature")

curvature_squared_relaxed_text = make_test_text(math.pi/6)
relaxer.relax(curvature_squared_relaxed_text, penalty_coefficients={"velocity": 0, "curvature": 0, "curvature_squared": 20})
render_with_comments(curvature_squared_relaxed_text, "Relaxed squares of max curvature")

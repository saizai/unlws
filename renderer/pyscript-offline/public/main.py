import math
from pyscript import document
from canvas import HTMLDOMCanvas
from emicSection import EmicSection
from glyphDictionary import SingleSVGGlyphDictionary
from relLine import RelLine
import relaxer

board = document.querySelector("#svgboard")

dictionary = SingleSVGGlyphDictionary('unlws_glyphs/glyphs.svg')

def make_test_text(I_angle_offset = 0, distance_multiplier = 1, name = "test text"):
    text = EmicSection(dictionary = dictionary, name = name)

    firstsg = dictionary.glyph_by_id("I")
    firstsg = relaxer.DifferentialSection.from_emic_section(firstsg)
    firstsg.x = -2. * distance_multiplier
    firstsg.y = 0.
    firstsg.angle = -math.pi/2 + I_angle_offset#math.pi/6#-math.pi/2
    text.add_subsection(firstsg)

    cat = dictionary.glyph_by_id("cat")
    cat = relaxer.DifferentialSection.from_emic_section(cat)
    cat.x = 2. * distance_multiplier
    cat.y = 0.
    cat.angle = math.pi
    text.add_subsection(cat)

    rel = RelLine(firstsg, "X", cat, "X")
    text.add_rel(rel)

    cat2 = dictionary.glyph_by_id("cat", name = "cat2")
    cat2 = relaxer.DifferentialSection.from_emic_section(cat2)
    cat2.x = 2. * distance_multiplier
    cat2.y = 1.
    cat2.angle = math.pi
    text.add_subsection(cat2)

    rel2 = RelLine(firstsg, "X", cat2, "X")
    text.add_rel(rel2)
    
    cat.dx = 1.
    cat2.dx = 1.
    
    return text

def render_with_comments(text, description, draw_bboxes = False):
    sub_board = document.createElement('div')
    canvas = HTMLDOMCanvas(sub_board)

    canvas.render(text, draw_bboxes = draw_bboxes)

    board.append(sub_board)


    p = document.createElement("p")
    p.innerHTML += f"{description}:<br>"
    # p.innerHTML += f"Non-constant-velocity penalty: {str(relaxer.total_penalty(text, {"velocity": 1, "curvature": 0, "distance": 0}))}.<br>"
    # p.innerHTML += f"Derivative for top rel: {str(relaxer.deriv_velocity_penalty(text.rels[0]))}.<br>"
    p.innerHTML += f"Curvature penalty: {str(relaxer.total_penalty(text, {"velocity": 0, "curvature": 1, "distance": 0}))}.<br>"
    p.innerHTML += f"Curvature squared penalty: {str(relaxer.total_penalty(text, {"velocity": 0, "curvature": 0, "distance": 0, "curvature_squared": 1}))}.<br>"
    # p.innerHTML += f"Curvature penalty for top rel: {str(relaxer.curvature_penalty(text.rels[0]))}.<br>"
    # p.innerHTML += f"Curvature penalty for bottom rel: {str(relaxer.curvature_penalty(text.rels[1]))}.<br>"

    board.append(p)

text = make_test_text(math.pi/6, name = "initial")
# render_with_comments(text, "Initial")

velocity_relaxed_text = make_test_text(math.pi/6, name = "velocity relaxed")

relaxer.relax(velocity_relaxed_text, penalty_coefficients={"velocity": 1, "curvature": 0})
render_with_comments(velocity_relaxed_text, "Relaxed velocity", draw_bboxes = True)

# curvature_relaxed_text = make_test_text(math.pi/6)
# relaxer.relax(curvature_relaxed_text, penalty_coefficients={"velocity": 0, "curvature": 5})
# render_with_comments(curvature_relaxed_text, "Relaxed max curvature")

curvature_squared_relaxed_text = make_test_text(math.pi/6, name = "curvature² relaxed")
curvature_squared_relaxed_text.color = "orange"
relaxer.relax(curvature_squared_relaxed_text, penalty_coefficients={"velocity": 0, "curvature": 0, "curvature_squared": 20})
# render_with_comments(curvature_squared_relaxed_text, "Relaxed squares of max curvature")

# Add BPs to the sections, so that they can be connected to eachother.
velocity_relaxed_text.addBP("X", velocity_relaxed_text.subsections[1].bp("X"))
velocity_relaxed_text.color = "blue"
curvature_squared_relaxed_text.addBP("X", curvature_squared_relaxed_text.subsections[2].bp("X"))

# Make a big text that has two subsections, both of which have their own subsections.
big_text = relaxer.DifferentialSection(dictionary = dictionary, name = "compound text")
# big_text.color = "black" # FIXME: doesn't work because the .unlws class overrides the <g> element's stroke.
big_text.add_subsection(velocity_relaxed_text)
big_text.add_subsection(curvature_squared_relaxed_text)

# Connect the subsections.
inter_section_rel = RelLine(velocity_relaxed_text, "X", curvature_squared_relaxed_text, "X")
big_text.add_rel(inter_section_rel)

relaxer.relax(big_text)

render_with_comments(big_text, "Compound text")

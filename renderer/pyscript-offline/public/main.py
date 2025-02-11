import math
from pyscript import document
from canvas import HTMLDOMCanvas
from emicSection import EmicSection
from glyphDictionary import SingleSVGGlyphDictionary
from relLine import RelLine
from bindingPoint import RelativeBindingPoint
import relaxer

board = document.querySelector("#svgboard")

dictionary = SingleSVGGlyphDictionary('unlws_glyphs/glyphs.svg')

def make_test_text(I_angle_offset = 0, distance_multiplier = 1, name = "test text"):
    text = EmicSection(dictionary = dictionary, name = name)

    text.angle = math.pi/2

    firstsg = dictionary.glyph_by_id("I")
    firstsg = relaxer.DifferentialSection.from_emic_section(firstsg)
    firstsg.x = -2. * distance_multiplier
    firstsg.y = 0.
    firstsg.angle = -math.pi/2 + I_angle_offset#math.pi/6#-math.pi/2
    firstsg_sec = relaxer.DifferentialSection(dictionary, "I wrapper")
    firstsg_sec.add_subsection(firstsg)
    text.add_subsection(firstsg_sec)

    cat = dictionary.glyph_by_id("cat")
    cat = relaxer.DifferentialSection.from_emic_section(cat)
    cat.x = 2. * distance_multiplier
    cat.y = 0.
    cat.angle = math.pi
    cat_sec = relaxer.DifferentialSection(dictionary, "cat wrapper")
    cat_sec.add_subsection(cat)
    cat_sec.angle = math.pi / 6
    text.add_subsection(cat_sec)
    
    cat_relative_bp = RelativeBindingPoint(cat, "X")
    text.addBP("cat bp", cat_relative_bp)
    
    # FIXME: why is the cat end of this rel horizontal (it thinks "cat" is rotated 90°, when it's really 30°)
    rel = RelLine(firstsg, "X", text, "cat bp")
    text.add_rel(rel)

    # cat2 = dictionary.glyph_by_id("cat", name = "cat2")
    # cat2 = relaxer.DifferentialSection.from_emic_section(cat2)
    # cat2.x = 2. * distance_multiplier
    # cat2.y = 1.
    # cat2.angle = math.pi
    # text.add_subsection(cat2)

    # rel2 = RelLine(firstsg, "X", cat2, "X")
    # text.add_rel(rel2)
    
    # cat.dx = 1.
    # cat2.dx = 1.
    
    return text

def render_with_comments(text, description, draw_bboxes = False):
    sub_board = document.createElement('div')
    canvas = HTMLDOMCanvas(sub_board)

    canvas.render(text, draw_bboxes = draw_bboxes)

    board.append(sub_board)


    p = document.createElement("p")
    p.innerHTML += f"{description}:<br>"
    p.innerHTML += f"BP positions: {[[(subsection.bp(bp_name).x, subsection.bp(bp_name).y) for bp_name in subsection.lemma_bps] for subsection in text.subsections]}.<br>"
    # p.innerHTML += f"Distance penalty: {str(relaxer.total_penalty(text, {"velocity": 0, "curvature": 0, "distance": 1}))}.<br>"
    # p.innerHTML += f"Non-constant-velocity penalty: {str(relaxer.total_penalty(text, {"velocity": 1, "curvature": 0, "distance": 0}))}.<br>"
    # p.innerHTML += f"Derivative for top rel: {str(relaxer.deriv_velocity_penalty(text.rels[0]))}.<br>"

    # p.innerHTML += f"Curvature penalty: {str(relaxer.total_penalty(text, {"velocity": 0, "curvature": 1, "distance": 0}))}.<br>"
    # p.innerHTML += f"Curvature squared penalty: {str(relaxer.total_penalty(text, {"velocity": 0, "curvature": 0, "distance": 0, "curvature_squared": 1}))}.<br>"
    
    # p.innerHTML += f"Curvature penalty for top rel: {str(relaxer.curvature_penalty(text.rels[0]))}.<br>"
    # p.innerHTML += f"Curvature penalty for bottom rel: {str(relaxer.curvature_penalty(text.rels[1]))}.<br>"

    board.append(p)

def render_relaxation_steps(text, name, penalty_coefficients={}, stepcount_per_iteration=50, iteration_count=4):
    render_with_comments(text, f"{name} initial", draw_bboxes=True)
    for i in range(iteration_count):
        relaxer.relax(text, step_count=stepcount_per_iteration, penalty_coefficients=penalty_coefficients)
        render_with_comments(text, f"{name} after {stepcount_per_iteration*(i+1)} steps", draw_bboxes=True)

for i in range(3):
    text = make_test_text(math.pi/6, name = "initial", distance_multiplier=i)
    render_with_comments(text, "Initial", draw_bboxes=True)

# text = make_test_text(math.pi/6, name = "initial")
# render_relaxation_steps(text, "Simple text", stepcount_per_iteration=30, iteration_count=3)





# subtext_1 = make_test_text(math.pi/6, name = "velocity relaxed")

# # relaxer.relax(subtext_1, penalty_coefficients={"velocity": 1, "curvature": 0})

# subtext_2 = make_test_text(math.pi/6, name = "curvature² relaxed")
# subtext_2.color = "orange"
# # relaxer.relax(subtext_2, penalty_coefficients={"velocity": 0, "curvature": 0, "curvature_squared": 20})

# # Add BPs to the sections, so that they can be connected to eachother.
# subtext_1.addBP("X", subtext_1.subsections[0].bp("X"))
# subtext_1.color = "blue"
# subtext_2.addBP("X", subtext_2.subsections[0].bp("X"))

# # Make a big text that has two subsections, both of which have their own subsections.
# big_text = relaxer.DifferentialSection(dictionary = dictionary, name = "compound text")
# # big_text.color = "black" # FIXME: doesn't work because the .unlws class overrides the <g> element's stroke.
# big_text.add_subsection(subtext_1)
# big_text.add_subsection(subtext_2)

# # Connect the subsections.
# inter_section_rel = RelLine(subtext_1, "X", subtext_2, "X")
# big_text.add_rel(inter_section_rel)

# render_relaxation_steps(big_text, "Compound text", stepcount_per_iteration=70)

import math
from emicSection import EmicSection
from glyphDictionary import SingleSVGGlyphDictionary
from relLine import RelLine
from bindingPoint import RelativeBindingPoint
import relaxer

class Main():
  def __init__(self, document):
    self.document = document
    self.body = self.document.body

    self.dictionary = SingleSVGGlyphDictionary('unlws_glyphs/glyphs.svg')

  def append_canvas(self):
    """Append a Canvas to body and return it."""
    raise NotImplementedError()
  
  def append_text(self, container, text):
    """Add `text` to `container` (an element in `document`) as a `<p>` node.
    Newlines can be made with `\\n`."""
    raise NotImplementedError()

  def make_test_text(self, angle_offset = 0, distance_multiplier = 1, name = "test text"):
    text = EmicSection(dictionary = self.dictionary, name = name)

    text.angle = math.pi/3 + angle_offset # FIXME: the cat end of the rel responds doubly to this changing.

    firstsg = self.dictionary.glyph_by_id("I")
    firstsg = relaxer.DifferentialSection.from_emic_section(firstsg)
    firstsg.x = -2. * distance_multiplier
    firstsg.y = 0.
    firstsg.angle = -math.pi/2#math.pi/6#-math.pi/2
    firstsg_sec = relaxer.DifferentialSection(self.dictionary, "I wrapper")
    firstsg_sec.add_subsection(firstsg)
    text.add_subsection(firstsg_sec)

    cat = self.dictionary.glyph_by_id("cat")
    cat = relaxer.DifferentialSection.from_emic_section(cat)
    cat.x = 2. * distance_multiplier
    cat.y = 0.
    cat.angle = math.pi
    cat_sec = relaxer.DifferentialSection(self.dictionary, "cat wrapper")
    cat_sec.add_subsection(cat)
    cat_sec.angle = math.pi/6 # FIXME: the rel should respond to this changing, but doesn't.
    text.add_subsection(cat_sec)
    
    cat_relative_bp = RelativeBindingPoint(cat, "X")
    text.addBP("cat bp", cat_relative_bp)
    
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

  def render_with_comments(self, text, description, draw_bboxes = False):
    canvas = self.append_canvas()
    canvas.render(text, draw_bboxes = draw_bboxes)

    comment = ""
    comment += f"{description}:\n"
    comment += f"BP positions: {[[[(round(subsection.subsections[0].bp(bp_name).x, 2), round(subsection.subsections[0].bp(bp_name).y, 2)) for bp_name in subsection.subsections[0].lemma_bps]] for subsection in text.subsections]}."

    self.append_text(canvas.parent, comment)

  def render_relaxation_steps(self, text, name, penalty_coefficients={}, stepcount_per_iteration=50, iteration_count=4):
    self.render_with_comments(text, f"{name} initial", draw_bboxes=True)
    for i in range(iteration_count):
      relaxer.relax(text, step_count=stepcount_per_iteration, penalty_coefficients=penalty_coefficients)
      self.render_with_comments(text, f"{name} after {stepcount_per_iteration*(i+1)} steps", draw_bboxes=True)



  def main(self):
    for i in range(4):
      degrees = i*30
      text = self.make_test_text(angle_offset=degrees*math.pi/180, name = "initial")
      self.render_with_comments(text, f"θ = {degrees}°", draw_bboxes=True)

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

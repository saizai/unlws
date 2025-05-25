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

  def glyph_by_id(self, id):
    """Create a DifferentialSection given the id of a glyph in the dictionary."""
    glyph = self.dictionary.glyph_by_id(id)
    glyph = relaxer.DifferentialSection.from_emic_section(glyph)
    return glyph


  def make_tree(self, num_levels, name):
    if num_levels == 0:
      cat = self.glyph_by_id("cat")
      cat.angle = math.pi
      return cat

    text = relaxer.DifferentialSection(dictionary = self.dictionary, name = name)

    junction = self.glyph_by_id("junction-TEMPORARY")
    text.add_subsection(junction, {"X2": "X"})
    junction.x = -1
    junction.angle = math.pi/3
    
    sub_text_1 = self.make_tree(num_levels-1, name+" 1")
    sub_text_2 = self.make_tree(num_levels-1, name+" 2")
    text.add_subsection(sub_text_1, {})
    text.add_subsection(sub_text_2, {})
    sub_text_1.x = 2
    sub_text_1.y = 2**num_levels/2
    sub_text_2.x = 2
    sub_text_2.y = -2**num_levels/2


    rel = RelLine(sub_text_1, "X", junction, "X1")
    text.add_rel(rel)
    rel = RelLine(sub_text_2, "X", junction, "X3")
    text.add_rel(rel)

    return text

  def make_test_text(self, angle_offset = 0, distance_multiplier = 1, name = "test text"):
    text = EmicSection(dictionary = self.dictionary, name = name)

    text.angle = math.pi/2

    firstsg = self.glyph_by_id("I")
    firstsg.y = 0.
    firstsg.x = -3. * distance_multiplier
    firstsg.angle = -math.pi/2#math.pi/6#-math.pi/2
    text.add_subsection(firstsg)

    tree = self.make_tree(3, "tree")
    text.add_subsection(tree, {})
    
    rel = RelLine(firstsg, "X", tree, "X")
    text.add_rel(rel)

    # cat2 = self.glyph_by_id("cat", name = "cat2")
    # cat2.x = 2. * distance_multiplier
    # cat2.y = 1.
    # cat2.angle = math.pi
    # text.add_subsection(cat2)

    # rel2 = RelLine(firstsg, "X", cat2, "X")
    # text.add_rel(rel2)
    
    # cat.dx = 1.
    # cat2.dx = 1.
    
    return text

  def render_with_comments(self, text, description, draw_extras = False):
    canvas = self.append_canvas()
    canvas.render(text, draw_bounding_disks=draw_extras, draw_BPs=draw_extras)

    comment = ""
    comment += f"{description}:\n"

    self.append_text(canvas.parent, comment)

  def render_relaxation_steps(self, text, name, penalty_coefficients={}, stepcount_per_iteration=50, iteration_count=4):
    self.render_with_comments(text, f"{name} initial", draw_extras=True)
    for i in range(iteration_count):
      relaxer.relax(text, step_count=stepcount_per_iteration, penalty_coefficients=penalty_coefficients)
      self.render_with_comments(text, f"{name} after {stepcount_per_iteration*(i+1)} steps", draw_extras=True)



  def main(self):
    # for i in range(4):
    #   degrees = i*30
    #   text = self.make_test_text(angle_offset=degrees*math.pi/180, name = "initial")
    #   self.render_with_comments(text, f"θ = {degrees}°", draw_extras=True)

    text = self.make_test_text(name = "initial")
    self.render_relaxation_steps(text, "Tree", stepcount_per_iteration=5, iteration_count=3)


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

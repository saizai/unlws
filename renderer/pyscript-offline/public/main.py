import math
from emicText import EmicText
from glyphDictionary import SingleSVGGlyphDictionary
from relLine import RelLine
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
    """Add `text` to `container` (an element in `document`) as a <p> node.
    Newlines can be made with `\\n`."""
    raise NotImplementedError()

  def make_test_text(self, I_angle_offset = 0, distance_multiplier = 1):
    text = EmicText()

    firstsg = self.dictionary.glyph_by_id("I")
    firstsg = relaxer.DifferentialGlyph.from_glyph(firstsg)
    firstsg.x = -2. * distance_multiplier
    firstsg.y = 0.
    firstsg.angle = -math.pi/2 + I_angle_offset#math.pi/6#-math.pi/2
    text.add_glyph(firstsg)

    cat = self.dictionary.glyph_by_id("cat")
    cat = relaxer.DifferentialGlyph.from_glyph(cat)
    cat.x = 2. * distance_multiplier
    cat.y = 0.
    cat.angle = math.pi
    text.add_glyph(cat)

    rel = RelLine(firstsg, "X", cat, "X")
    text.add_rel(rel)

    cat2 = self.dictionary.glyph_by_id("cat")
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

  def render_with_comments(self, text, description):
    canvas = self.append_canvas()
    canvas.render(text)

    comment = f"{description}:\n"
    comment += f"Curvature penalty: { relaxer.total_penalty(text, {"velocity": 0, "curvature": 1, "distance": 0})}.\n"
    comment += f"Curvature squared penalty: { relaxer.total_penalty(text, {"velocity": 0, "curvature": 0, "distance": 0, "curvature_squared": 1})}.\n"
    comment += f"Curvature penalty for top rel: { relaxer.curvature_penalty(text.rels[0])}.\n"
    comment += f"Curvature penalty for bottom rel: { relaxer.curvature_penalty(text.rels[1])}."

    self.append_text(canvas.parent, comment)


  def main(self):
    text = self.make_test_text(math.pi/6)
    self.render_with_comments(text, "Initial")

    velocity_relaxed_text = self.make_test_text(math.pi/6)
    relaxer.relax(velocity_relaxed_text, penalty_coefficients={"velocity": 1, "curvature": 0})
    self.render_with_comments(velocity_relaxed_text, "Relaxed velocity")

    curvature_relaxed_text = self.make_test_text(math.pi/6)
    relaxer.relax(curvature_relaxed_text, penalty_coefficients={"velocity": 0, "curvature": 5})
    self.render_with_comments(curvature_relaxed_text, "Relaxed max curvature")

    curvature_squared_relaxed_text = self.make_test_text(math.pi/6)
    relaxer.relax(curvature_squared_relaxed_text, penalty_coefficients={"velocity": 0, "curvature": 0, "curvature_squared": 20})
    self.render_with_comments(curvature_squared_relaxed_text, "Relaxed squares of max curvature")

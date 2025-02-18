import math
from emicText import EmicText
from glyphDictionary import SingleSVGGlyphDictionary
from relLine import RelLine
import relaxer

class Main():
  def __init__(self, document, append_canvas, append_text):
    self.document = document
    self.body = self.document.body
    self.append_canvas = append_canvas
    self.append_text = append_text

    self.dictionary = SingleSVGGlyphDictionary('unlws_glyphs/glyphs.svg')


  def make_test_text(self):
    text = EmicText()
    
    firstsg = self.dictionary.glyph_by_id("I")
    firstsg = relaxer.DifferentialGlyph.from_glyph(firstsg)
    firstsg.x = -2.
    firstsg.y = 0.
    firstsg.angle = math.pi/6#-math.pi/2
    text.add_glyph(firstsg)

    cat = self.dictionary.glyph_by_id("cat")
    cat = relaxer.DifferentialGlyph.from_glyph(cat)
    cat.x = 2.
    cat.y = 0.
    cat.angle = math.pi
    text.add_glyph(cat)

    rel = RelLine(firstsg, "X", cat, "X")
    text.add_rel(rel)
    
    firstsg.dangle = 1.

    return text

  def render_with_comments(self, text):
    canvas = self.append_canvas()
    canvas.render(text)

    comment = ""
    comment += f"Max curvatures: { [relaxer.curvature_penalty(rel) for rel in text.rels] }. "
    comment += f"Derivatives: { [relaxer.deriv_curvature_penalty(rel) for rel in text.rels] }. "

    self.append_text(canvas.parent, comment)

  def main(self):
    text = self.make_test_text()
    self.render_with_comments(text)

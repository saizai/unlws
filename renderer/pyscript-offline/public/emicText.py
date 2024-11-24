import re
import xml.dom.minidom as minidom
from glyphDictionary import SingleSVGGlyphDictionary

class EmicText:
  """An UNLWS sentence, with the layout of how it sits on the page,"""
  
  def __init__(self):
    self.glyphs = [] # glyphs in the sentence
    self.rels = [] # rels in the sentence
    
    # FIXME: style does not belong in the dictionary
    dictionary = SingleSVGGlyphDictionary('unlws_glyphs/glyphs.svg')
    self.style = dictionary.style
    # default SVG class for UNLWS text, to be used with the style
    self.text_class = dictionary.text_class
  
  def add_glyph(self, glyph):
    self.glyphs.append(glyph)
  
  def add_rel(self, rel):
    self.rels.append(rel)
  
  @property
  def default_stroke_width(self):
    "The default stroke width according to the style of this text."
    # FIXME: this is a crude and brittle inspection of the CSS. Do better.
    # E.g. look for self.text_class as a selector.
    css = self.style.childNodes[0].data
    span = re.search('stroke-width\\s*:\\s*([-+0-9.eE]*)', css).span(1)
    return float(css[span[0]:span[1]])
  
  def bounding_box(self):
    """Return the bounding box of this sentence, as a 4-tuple
    (xmin, xmax, ymin, ymax)."""
    bboxes = [glyph.bounding_box(stroke_width_allowance=self.default_stroke_width)
        for glyph in self.glyphs] +\
      [rel.bounding_box(stroke_width_allowance=self.default_stroke_width)
        for rel in self.rels]
    return (
            min(b[0] for b in bboxes),
            max(b[1] for b in bboxes),
            min(b[2] for b in bboxes),
            max(b[3] for b in bboxes),
            )
  
  def svg(self):
    """Return an SVG of this sentence as XML."""
    svg = minidom.getDOMImplementation().createDocument("http://www.w3.org/2000/svg", "svg", None)
    svg.documentElement.setAttribute("xmlns", "http://www.w3.org/2000/svg")
    svg.documentElement.setAttribute("xmlns:unlws-renderer", "https://github.com/saizai/unlws")
    bbox = self.bounding_box()
    svg.documentElement.setAttribute("viewBox", f"{bbox[0]} {bbox[2]} {bbox[1]-bbox[0]} {bbox[3]-bbox[2]}")
    # for now, magic scaling of 32px per UNLWS em
    svg.documentElement.setAttribute("width", str(int(32*(bbox[1]-bbox[0])))+"px")

    svg.documentElement.appendChild(self.style)
    
    for glyph in self.glyphs:
      ## test: show bounding box
      #bbox = glyph.bounding_box(stroke_width_allowance=self.default_stroke_width)
      #r = svg.createElement("rect")
      #r.setAttribute("x", str(bbox[0]))
      #r.setAttribute("width", str(bbox[1]-bbox[0]))
      #r.setAttribute("y", str(bbox[2]))
      #r.setAttribute("height", str(bbox[3]-bbox[2]))
      #r.setAttribute("fill", "none")
      #r.setAttribute("stroke", "green")
      #r.setAttribute("stroke-width", str(1./36))
      #svg.documentElement.appendChild(r)
      el = glyph.svg()
      el.setAttribute("class", self.text_class)
      svg.documentElement.appendChild(el)
    for rel in self.rels:
      ## test: show bounding box
      #bbox = rel.bounding_box(stroke_width_allowance=self.default_stroke_width)
      #r = svg.createElement("rect")
      #r.setAttribute("x", str(bbox[0]))
      #r.setAttribute("width", str(bbox[1]-bbox[0]))
      #r.setAttribute("y", str(bbox[2]))
      #r.setAttribute("height", str(bbox[3]-bbox[2]))
      #r.setAttribute("fill", "none")
      #r.setAttribute("stroke", "red")
      #r.setAttribute("stroke-width", str(1./36))
      #svg.documentElement.appendChild(r)
      el = rel.svg()
      el.setAttribute("class", self.text_class)
      svg.documentElement.appendChild(el)
    
    return svg

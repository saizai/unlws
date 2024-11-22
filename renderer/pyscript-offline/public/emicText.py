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
  
  def add_glyph(self, glyph):
    self.glyphs.append(glyph)
  
  def add_rel(self, rel):
    self.rels.append(rel)
  
  @property
  def default_stroke_width(self):
    "The default stroke width according to the style of this text."
    # FIXME: this is a crude and brittle inspection of the CSS. Do better.
    css = self.style.childNodes[0].data
    span = re.search('stroke-width\\s*:\\s*([-+0-9.eE]*)', css).span(1)
    return float(css[span[0]:span[1]])
  
  def svg(self):
    """Return an SVG of this sentence as XML."""
    # TODO: For the moment this just returns a fixed test SVG.
    # The operations herein should be refactored into
    # dictionary handling, etc.
    
    svg = minidom.getDOMImplementation().createDocument("http://www.w3.org/2000/svg", "svg", None)
    svg.documentElement.setAttribute("xmlns", "http://www.w3.org/2000/svg")
    svg.documentElement.setAttribute("xmlns:unlws-renderer", "https://github.com/saizai/unlws")
    svg.documentElement.setAttribute("width", "192px")
    svg.documentElement.setAttribute("viewBox", "-3 -2 6 4")
    
    svg.documentElement.appendChild(self.style)
    
    for glyph in self.glyphs:
      svg.documentElement.appendChild(glyph.svg())
    for rel in self.rels:
      ## test: show bounding box
      #bbox = rel.boundingBox()
      #r = svg.createElement("rect")
      #r.setAttribute("x", str(bbox[0]))
      #r.setAttribute("width", str(bbox[1]-bbox[0]))
      #r.setAttribute("y", str(bbox[2]))
      #r.setAttribute("height", str(bbox[3]-bbox[2]))
      #r.setAttribute("fill", "none")
      #r.setAttribute("stroke", "red")
      #r.setAttribute("stroke-width", str(1./36))
      #svg.documentElement.appendChild(r)
      svg.documentElement.appendChild(rel.svg())
    
    return svg

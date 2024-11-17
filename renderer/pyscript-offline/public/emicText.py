import xml.dom.minidom as minidom
from glyphDictionary import SingleSVGGlyphDictionary

class EmicText:
  """An UNLWS sentence, with the layout of how it sits on the page,"""
  
  def __init__(self):
    self.glyphs = [] # glyphs in the sentence
    
    # FIXME: style does not belong in the dictionary
    dictionary = SingleSVGGlyphDictionary('unlws_glyphs/glyphs.svg')
    self.style = dictionary.style
  
  def add_glyph(self, glyph):
    self.glyphs.append(glyph)
  
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
    
    return svg

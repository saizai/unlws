import math
import xml.dom.minidom as minidom
from glyphDictionary import SingleSVGGlyphDictionary

class EmicText:
  """An UNLWS sentence, with the layout of how it sits on the page,"""
  
  # TODO: implement this
  
  def svg(self):
    """Return an SVG of this sentence as XML."""
    # TODO: For the moment this just returns a fixed test SVG.
    # The operations herein should be refactored into
    # dictionary handling, etc.
    
    dictionary = SingleSVGGlyphDictionary('unlws_glyphs/glyphs.svg')
    
    svg = minidom.getDOMImplementation().createDocument("http://www.w3.org/2000/svg", "svg", None)
    svg.documentElement.setAttribute("xmlns", "http://www.w3.org/2000/svg")
    svg.documentElement.setAttribute("xmlns:unlws-renderer", "https://github.com/saizai/unlws")
    svg.documentElement.setAttribute("width", "192px")
    svg.documentElement.setAttribute("viewBox", "-3 -2 6 4")
    
    svg.documentElement.appendChild(dictionary.style)
    
    firstsg = dictionary.glyph_by_id("I")
    firstsg.x = -2.
    firstsg.y = 0.
    firstsg.angle = -math.pi/2
    #firstsg_elt.setAttribute("transform", "translate(-2 0) rotate(-90)")
    svg.documentElement.appendChild(firstsg.svg())
    
    cat = dictionary.glyph_by_id("cat")
    cat.x = 2.
    cat.y = 0.
    cat.angle = math.pi
    #cat_elt.setAttribute("transform", "translate(2 0) rotate(180)")
    svg.documentElement.appendChild(cat.svg())
    
    return svg

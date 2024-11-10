from copy import deepcopy
import xml.dom.minidom as minidom

class EmicText:
  """An UNLWS sentence, with the layout of how it sits on the page,"""
  
  # TODO: implement this
  
  def svg(self):
    """Return an SVG of this sentence as XML."""
    # TODO: For the moment this just returns a fixed test SVG.
    # The operations herein should be refactored into
    # dictionary handling, etc.
    
    dictionary = minidom.parse('unlws_glyphs/glyphs.svg')
    # There might be other g elements, but this should include all glyphs:
    glyphs = dictionary.getElementsByTagName("g")
    
    svg = minidom.getDOMImplementation().createDocument("http://www.w3.org/2000/svg", "svg", None)
    svg.documentElement.setAttribute("xmlns", "http://www.w3.org/2000/svg")
    svg.documentElement.setAttribute("xmlns:unlws-renderer", "https://github.com/saizai/unlws")
    svg.documentElement.setAttribute("width", "192px")
    svg.documentElement.setAttribute("viewBox", "-3 -2 6 4")
    
    # FIXME: the dictionary isn't the right place to store style information
    style = dictionary.getElementsByTagName("style")[0]
    svg.documentElement.appendChild(style)
    
    # I hope copy.deepcopy acts OK on DOM objects.  It looks to.
    firstsg = deepcopy([g for g in glyphs if g.getAttribute("id") == "I"][0])
    firstsg.setAttribute("transform", "translate(-2 0) rotate(-90)")
    svg.documentElement.appendChild(firstsg)
    
    cat = deepcopy([g for g in glyphs if g.getAttribute("id") == "cat"][0])
    cat.setAttribute("transform", "translate(2 0) rotate(180)")
    svg.documentElement.appendChild(cat)

    return svg

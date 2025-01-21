import re
import xml.dom.minidom as minidom
from glyphDictionary import SingleSVGGlyphDictionary
from emicSection import EmicSection

# TODO: do we want this? Perhaps all the funcionality should be included in all EmicSections
class EmicText(EmicSection):
  """An UNLWS sentence, with the layout of how it sits on the page,"""
  
  def __init__(self):
    super().__init__()

    # FIXME: style does not belong in the dictionary
    dictionary = SingleSVGGlyphDictionary('unlws_glyphs/glyphs.svg')
    self.style = dictionary.style
    # default SVG class for UNLWS text, to be used with the style
    self.text_class = dictionary.text_class
  
  @property
  def default_stroke_width(self):
    "The default stroke width according to the style of this text."
    # FIXME: this is a crude and brittle inspection of the CSS. Do better.
    # E.g. look for self.text_class as a selector.
    css = self.style.childNodes[0].data
    span = re.search('stroke-width\\s*:\\s*([-+0-9.eE]*)', css).span(1)
    return float(css[span[0]:span[1]])

  def svg(self):
    """Return an SVG of this section as an XML <g> element."""
    svg = minidom.getDOMImplementation().createDocument("http://www.w3.org/2000/svg", "svg", None)
    document = svg.documentElement
    
    document.setAttribute("xmlns", "http://www.w3.org/2000/svg")
    document.setAttribute("xmlns:unlws-renderer", "https://github.com/saizai/unlws")
    bbox = self.bounding_box()
    document.setAttribute("viewBox", f"{bbox[0]} {bbox[2]} {bbox[1]-bbox[0]} {bbox[3]-bbox[2]}")
    # for now, magic scaling of 32px per UNLWS em
    document.setAttribute("width", str(int(32*(bbox[1]-bbox[0])))+"px")

    document.appendChild(self.style)
    
    contents = super().svg()
    document.appendChild(contents)
    
    return svg

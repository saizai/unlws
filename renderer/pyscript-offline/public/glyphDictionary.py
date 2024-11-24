from copy import deepcopy
import math
import xml.dom.minidom as minidom
from glyph import BindingPoint, Glyph

class GlyphDictionary:
  """An abstract class to retrieve glyphs from storage."""
  pass

class SingleSVGGlyphDictionary(GlyphDictionary):
  """A GlyphDictionary held in a single SVG.
  
  The glyphs are g children of a top-level defs element,
  labelled with names in the id property.
  These have properties in the unlws-renderer namespace, after Talisoso."""
  
  def __init__(self, filename):
    self.dictionary = minidom.parse(filename)
    # There might be other g elements, but this should include all glyphs:
    self.glyphs = self.dictionary.getElementsByTagName("g")
    
    self._style = self.dictionary.getElementsByTagName("style")[0]
    settings = self.dictionary.getElementsByTagName("unlws-renderer:settings")[0]
    # default SVG class for UNLWS text, to be used with the style
    self.text_class = settings.getAttribute("text-class")
  
  # FIXME: Style should be stored somewhere better than the dictionary.
  # (Although since SVG expects paths to be filled by default,
  # it is sensible to put path {fill: none} in the dictionary.
  # That should be separated from other style features.)
  @property
  def style(self):
    return self._style
  
  def glyph_by_id(self, id):
    """Return the dictionary form of the glyph with id `id`.
    
    Strip the dictionary apparatus."""
    g_elt = deepcopy([g for g in self.glyphs if g.getAttribute("id") == id][0])
    g_elt.removeAttribute("id")
    glyph = Glyph(g_elt)
    
    # Unpack the properties in the unlws-renderer namespace.
    for child in g_elt.childNodes:
      if child.nodeType == child.ELEMENT_NODE and child.tagName == "unlws-renderer:bp":
        bp = BindingPoint(
                          x = float(child.getAttribute("x")),
                          y = float(child.getAttribute("y")),
                          angle = float(child.getAttribute("angle"))/180*math.pi
                          )
        glyph.addBP(child.getAttribute("name"), bp)
        g_elt.removeChild(child)
        child.unlink() # TODO: test this wrt deep copying
    
    return glyph


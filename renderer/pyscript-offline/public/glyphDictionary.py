from copy import deepcopy
import xml.dom.minidom as minidom
from glyph import Glyph

class GlyphDictionary:
  """An abstract class to retrieve glyphs from storage."""
  pass

class SingleSVGGlyphDictionary(GlyphDictionary):
  """A GlyphDictionary held in a single SVG.
  
  The glyphs are g children of a top-level defs element,
  labelled with names in the id property."""
  
  def __init__(self, filename):
    self.dictionary = minidom.parse(filename)
    # There might be other g elements, but this should include all glyphs:
    self.glyphs = self.dictionary.getElementsByTagName("g")
    self._style = self.dictionary.getElementsByTagName("style")[0]
  
  # FIXME: Style should be stored somewhere better than the dictionary.
  # (Although since SVG expects paths to be filled by default,
  # it is sensible to put path {fill: none} in the dictionary.
  # That should be separated from other style features.)
  @property
  def style(self):
    return self._style
  
  def glyph_by_id(self, id):
    g_elt = deepcopy([g for g in self.glyphs if g.getAttribute("id") == id][0])
    g_elt.removeAttribute("id")
    return Glyph(g_elt)


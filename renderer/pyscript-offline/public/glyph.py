from copy import deepcopy
import math
import xml.dom.minidom as minidom

class Glyph:
  """An instance of a glyph within a text."""
  
  def __init__(self, lemma_svg = None):
    """Initialise this glyph to have  lemma_svg  as its form."""
    # lemma_svg should be a g element which does not have a transform.
    self.lemma_svg = lemma_svg
    if self.lemma_svg == None:
      # minidom won't create an element without a document.
      document = minidom.getDOMImplementation().createDocument("http://www.w3.org/2000/svg", "svg", None)
      self.lemma_svg = document.createElement("g")
    
    # Position in the sentence, in svg-style coordinates where
    # x increases right and y increases down.
    self.x = 0.
    self.y = 0.
    # Angle of rotation of the glyph, in *radians*.
    # A positive angle is a clockwise rotation, to match the reflected y.
    self.angle = 0.
  
  def svg(self):
    surface_svg = deepcopy(self.lemma_svg)
    surface_svg.setAttribute("transform", f"translate({self.x} {self.y}) rotate({self.angle*180./math.pi})")
    return surface_svg

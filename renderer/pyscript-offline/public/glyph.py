from copy import deepcopy
import math
import xml.dom.minidom as minidom
import svgpathtools
from BPHaver import BPHaver

class Glyph(BPHaver):
  """A lemma glyph."""
  
  def __init__(self, lemma_svg = None):
    """Initialise this glyph to have  lemma_svg  as its form."""
    super().__init__()

    # lemma_svg should be a g element which does not have a transform.
    self.lemma_svg = lemma_svg
    if self.lemma_svg == None:
      # minidom won't create an element without a document.
      document = minidom.getDOMImplementation().createDocument("http://www.w3.org/2000/svg", "svg", None)
      self.lemma_svg = document.createElement("g")

def snap_to_end(path_list, x, y, eps = 1e-3):
  """If (x, y) is near either end of a path in path_list, return the endpoint
  and an outgoing handle end, as a 4-tuple (end x, end y, handle x, handle y).
  The outgoing handle end goes in the opposite direction, to allow for nicely
  extending a stroke.
  
  If no matches, return (x, y, None, None).
  
  If the end segment of the path is a cubic spline, match the length of the
  handle. If it's a line, normalise the length of the handle.
  
  Arguments:
  path_list: the list of svgpathtools paths
  (x, y): the point to look for
  eps: tolerance (in the 2-norm)"""
  z = x+y*(0+1j)
  for path in path_list:
    if abs(path.start - z) <= eps:
      derivative = -path[0].derivative(0)/3 # /3 because cubic
      if isinstance(path[0], svgpathtools.Line):
        derivative /= abs(derivative) # normalise
      handlez = path.start + derivative
      return path.start.real, path.start.imag, handlez.real, handlez.imag
    if abs(path.end - z) <= eps:
      derivative = path[-1].derivative(1)/3 # /3 because cubic
      if isinstance(path[-1], svgpathtools.Line):
        derivative /= abs(derivative) # normalise
      handlez = path.end + derivative
      return path.end.real, path.end.imag, handlez.real, handlez.imag
  
  return x, y, None, None

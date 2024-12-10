from copy import deepcopy
import math
import xml.dom.minidom as minidom
import svgpathtools
from bindingPoint import BindingPoint

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
    # Angle of rotation of the glyph, in *radians*.  0 is rightward.
    # A positive angle is a clockwise rotation, to match the reflected y.
    self.angle = 0.
    
    # Binding points, as a hash from name to BP object.
    # Stored in the coordinates of the lemma form, rather than as transformed.
    self.lemma_bps = {}
  
  @property
  def angle_in_degrees(self):
    "Rotation of this glyph in degrees."
    return self.angle*180./math.pi
  
  @property
  def z(self):
    "Translation of this glyph as a complex number."
    return self.x+self.y*(0+1j)
  
  def addBP(self, name, bp):
    """Add `bp` with the name `name`."""
    bp.host = self
    bp.name = name
    self.lemma_bps[name] = bp
  
  def bp(self, name):
    """Return the BP `name`, in sentence coordinates with transformation applied."""
    return self.lemma_bps[name].rotate(self.angle).translate(self.x, self.y)
  
  def svg(self, drawBPs = False):
    """Return a rendered SVG, with the correct coordinate transform.
    
    If `drawBPs` is true, draw the BPs as green circles."""
    surface_svg = deepcopy(self.lemma_svg)
    surface_svg.setAttribute("transform", f"translate({self.x} {self.y}) rotate({self.angle_in_degrees})")
    
    if drawBPs:
      # Again create a document, urgh.
      document = minidom.getDOMImplementation().createDocument("http://www.w3.org/2000/svg", "svg", None)
      for bp in self.lemma_bps.values():
        dot = document.createElement("circle")
        dot.setAttribute("cx", str(bp.x))
        dot.setAttribute("cy", str(bp.y))
        dot.setAttribute("r", str(1./6)) # magic width based on default stroke width
        dot.setAttribute("fill", "#6aa84f")
        dot.setAttribute("stroke", "none")
        surface_svg.appendChild(dot)
        # The end of a stubby line for the handle. Again the length 1/3 is magic.
        endx = (2*bp.x + bp.handlex)/3
        endy = (2*bp.y + bp.handley)/3
        stub = document.createElement("line")
        stub.setAttribute("x1", str(bp.x))
        stub.setAttribute("y1", str(bp.y))
        stub.setAttribute("x2", str(endx))
        stub.setAttribute("y2", str(endy))
        stub.setAttribute("stroke", "#6aa84f")
        stub.setAttribute("stroke-width", str(1./12)) # like the dictionary's style
        surface_svg.appendChild(stub)
    
    return surface_svg
  
  def svgpathtools_paths(self):
    """Return a list of svgpathtools Path objects represented by this glyph.
    
    The Path objects returned are in global svg coordinates."""
    # Code patterned on the svg2paths function in svgpathtools.
    # That has a file read baked in which means we can't use it directly.
    # TODO: we may want to keep the attributes.
    def dom2dict(element):
        """Converts DOM elements to dictionaries of attributes."""
        keys = list(element.attributes.keys())
        values = [val.value for val in list(element.attributes.values())]
        return dict(list(zip(keys, values)))
    
    d_strings = [el.getAttribute('d')
        for el in self.lemma_svg.getElementsByTagName('path')]
    d_strings += [svgpathtools.polyline2pathd(dom2dict(el))
        for el in self.lemma_svg.getElementsByTagName('polyline')]
    d_strings += [svgpathtools.polygon2pathd(dom2dict(el))
        for el in self.lemma_svg.getElementsByTagName('polygon')]
    d_strings += [('M' + l.getAttribute('x1') + ' ' + l.getAttribute('y1') +
                   'L' + l.getAttribute('x2') + ' ' + l.getAttribute('y2'))
        for el in self.lemma_svg.getElementsByTagName('line')]
    d_strings += [svgpathtools.ellipse2pathd(dom2dict(el))
        for el in self.lemma_svg.getElementsByTagName('ellipse')]
    d_strings += [svgpathtools.ellipse2pathd(dom2dict(el))
        for el in self.lemma_svg.getElementsByTagName('circle')]
    d_strings += [svgpathtools.rect2pathd(dom2dict(el))
        for el in self.lemma_svg.getElementsByTagName('rect')]
    
    path_list = [svgpathtools.parse_path(d) for d in d_strings]
    return [p.rotated(self.angle_in_degrees, origin=0+0j).translated(self.z)
        for p in path_list]
  
  def bounding_box(self, stroke_width_allowance = 0.):
    """Return the bounding box for this glyph, as a 4-tuple
    (xmin, xmax, ymin, ymax).
    
    Arguments:
    stroke_width_allowance: pad the bounding box by this much on each side,
      to allow for stroke width"""
    path_bboxes = [p.bbox() for p in self.svgpathtools_paths()]
    sbox = (
            min(b[0] for b in path_bboxes),
            max(b[1] for b in path_bboxes),
            min(b[2] for b in path_bboxes),
            max(b[3] for b in path_bboxes),
            )
    return (
            sbox[0]-stroke_width_allowance,
            sbox[1]+stroke_width_allowance,
            sbox[2]-stroke_width_allowance,
            sbox[3]+stroke_width_allowance,
            )

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

from copy import copy, deepcopy
import math
import xml.dom.minidom as minidom

class BindingPoint:
  """An instance of a binding point, either within a glyph or a larger text.
  
  Properties:
  host: the glyph this BP belongs to
  name: the name of this BP within `host`"""
  def __init__(self, x = 0., y = 0., handlex = None, handley = None,
      angle = None, speed = 1.):
    """Arguments:
    x, y: coordinates in svg conventions
    handlex, handley: coordinates of the spline handle
    angle: angle in radians, 0 is rightward, positive is clockwise
    speed: distance between the BP itself and its handle"""
    self.x = x
    self.y = y
    if handlex != None and handley != None:
      self.handlex = handlex
      self.handley = handley
    else:
      if angle == None: angle = 0. # some default
      self.handlex = x + speed * math.cos(angle)
      self.handley = y + speed * math.sin(angle)
  
  def translate(self, dx, dy):
    """Return a cooy of this BP translated by (dx, dy)."""
    p = copy(self)
    p.x += dx
    p.y += dy
    p.handlex += dx
    p.handley += dy
    return p
  
  def rotate(self, dangle):
    """Return a cooy of this BP rotated around the origin by dangle."""
    c, s = math.cos(dangle), math.sin(dangle)
    p = copy(self)
    p.x = c*self.x - s*self.y
    p.y = s*self.x + c*self.y
    p.handlex = c*self.handlex - s*self.handley
    p.handley = s*self.handlex + c*self.handley
    return p

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
  
  def addBP(self, name, bp):
    """Add a BP named `name` and positioned at `bp` within the lemma form."""
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
    surface_svg.setAttribute("transform", f"translate({self.x} {self.y}) rotate({self.angle*180./math.pi})")
    
    if drawBPs:
      # Again create a document, urgh.
      document = minidom.getDOMImplementation().createDocument("http://www.w3.org/2000/svg", "svg", None)
      for bp in self.lemma_bps.values():
        dot = document.createElement("circle")
        dot.setAttribute("cx", str(bp.x))
        dot.setAttribute("cy", str(bp.y))
        dot.setAttribute("r", str(1./6)) # magic width based on default stroke width
        dot.setAttribute("fill", "#6aa84f")
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

import xml.dom.minidom as minidom
import svgpathtools

class RelLine:
  """A rel line, connecting two BPs in an UNLWS sentence.
  
  The BPs are accessed 'by reference' using argument names, so that 
  changes to the sections propagate."""
  def __init__(self, section0, arg0, section1, arg1):
    "Create a rel between the BP of section0 named arg0 and that of section1 named arg1."
    self.section0 = section0
    self.arg0 = arg0
    self.section1 = section1
    self.arg1 = arg1
  
  @property
  def bp0(self):
    "The BP at the start of this rel line."
    return self.section0.bp(self.arg0)
  
  @property
  def bp1(self):
    "The BP at the end of this rel line."
    return self.section1.bp(self.arg1)
  
  def svg(self):
    # do I really need to create documents all the time?
    document = minidom.getDOMImplementation().createDocument("http://www.w3.org/2000/svg", "svg", None)
    path = document.createElement("path")
    path.setAttribute("d", f"M{self.bp0.x} {self.bp0.y}C{self.bp0.handlex} {self.bp0.handley} {self.bp1.handlex} {self.bp1.handley} {self.bp1.x} {self.bp1.y}")
    return path
  
  def svgpathtools_bezier(self):
    "Returns this rel line as a svgpathtools path."
    return svgpathtools.CubicBezier(
        self.bp0.z, self.bp0.handlez, self.bp1.handlez, self.bp1.z
      )
  
  def bounding_box(self, stroke_width_allowance = 0.):
    """Returns the bounding box for this rel line, as a 4-tuple
    (xmin, xmax, ymin, ymax).
    
    Arguments:
    stroke_width_allowance: pad the bounding box by this much on each side,
      to allow for stroke width"""
    sbox = self.svgpathtools_bezier().bbox()
    return (
            sbox[0]-stroke_width_allowance,
            sbox[1]+stroke_width_allowance,
            sbox[2]-stroke_width_allowance,
            sbox[3]+stroke_width_allowance,
            )

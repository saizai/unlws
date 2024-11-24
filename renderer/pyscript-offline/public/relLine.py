import xml.dom.minidom as minidom
import svgpathtools

class RelLine:
  """A rel line, connecting two BPs in an UNLWS sentence.
  
  Properties:
  bp1: start BP
  bp2: end BP"""
  def __init__(self, bp1, bp2):
    self.bp1 = bp1
    self.bp2 = bp2
  
  def svg(self):
    # do I really need to create documents all the time?
    document = minidom.getDOMImplementation().createDocument("http://www.w3.org/2000/svg", "svg", None)
    path = document.createElement("path")
    path.setAttribute("d", f"M{self.bp1.x} {self.bp1.y}C{self.bp1.handlex} {self.bp1.handley} {self.bp2.handlex} {self.bp2.handley} {self.bp2.x} {self.bp2.y}")
    return path
  
  def bounding_box(self, stroke_width_allowance = 0.):
    """Returns the bounding box for this rel line, as a 4-tuple
    (xmin, xmax, ymin, ymax).
    
    Arguments:
    stroke_width_allowance: pad the bounding box by this much on each side,
      to allow for stroke width"""
    sbox = svgpathtools.CubicBezier(
        self.bp1.z, self.bp1.handlez, self.bp2.handlez, self.bp2.z
      ).bbox()
    return (
            sbox[0]-stroke_width_allowance,
            sbox[1]+stroke_width_allowance,
            sbox[2]-stroke_width_allowance,
            sbox[3]+stroke_width_allowance,
            )

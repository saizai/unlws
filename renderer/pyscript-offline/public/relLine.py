import xml.dom.minidom as minidom
import svgpathtools

class RelLine:
  """A rel line, connecting two BPs in an UNLWS sentence.
  
  Properties:
  bp1: start BP
  bp2: end BP
  stroke_width: stroke width in svg units, for now assumed uniform"""
  def __init__(self, bp1, bp2, stroke_width = 1./12):
    # 1./12 is the default stroke width in our usual plain style
    self.bp1 = bp1
    self.bp2 = bp2
    self.stroke_width = stroke_width
  
  def svg(self):
    # do I really need to create documents all the time?
    document = minidom.getDOMImplementation().createDocument("http://www.w3.org/2000/svg", "svg", None)
    path = document.createElement("path")
    path.setAttribute("d", f"M{self.bp1.x} {self.bp1.y}C{self.bp1.handlex} {self.bp1.handley} {self.bp2.handlex} {self.bp2.handley} {self.bp2.x} {self.bp2.y}")
    # FIXME: stroke width is overridden by the style at present
    path.setAttribute("stroke-width", str(self.stroke_width))
    return path
  
  def boundingBox(self):
    """Returns the bounding box for this rel line, as a 4-tuple
    (xmin, xmax, ymin, ymax)."""
    sbox = svgpathtools.CubicBezier(
        self.bp1.z, self.bp1.handlez, self.bp2.handlez, self.bp2.z
      ).bbox()
    return (
            sbox[0]-self.stroke_width,
            sbox[1]+self.stroke_width,
            sbox[2]-self.stroke_width,
            sbox[3]+self.stroke_width,
            )

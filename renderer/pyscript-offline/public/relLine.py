import xml.dom.minidom as minidom

class RelLine:
  "A rel line, connecting two BPs in an UNLWS sentence."
  def __init__(self, bp1, bp2):
    self.bp1 = bp1
    self.bp2 = bp2
  
  def svg(self):
    # do I really need to create documents all the time?
    document = minidom.getDOMImplementation().createDocument("http://www.w3.org/2000/svg", "svg", None)
    path = document.createElement("path")
    path.setAttribute("d", f"M{self.bp1.x} {self.bp1.y}C{self.bp1.handlex} {self.bp1.handley} {self.bp2.handlex} {self.bp2.handley} {self.bp2.x} {self.bp2.y}")
    return path

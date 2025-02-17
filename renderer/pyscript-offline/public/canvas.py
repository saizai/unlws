class Canvas:
  """A canvas into which a rendered UNLWS sentence can be output.
  
  Do not confuse with the HTML canvas element (which we do not expect to use.)"""
  
  def render(self, emicsection):
    """Draw the EmicSection emicsection to this canvas."""
    raise NotImplementedError

class HTMLDOMCanvas(Canvas):
  """An element within the DOM as a Canvas, which we write an SVG inside."""
  
  def __init__(self, element):
    # element should be a JsProxy
    self.element = element
  
  def render(self, emicsection, draw_bboxes = False):
    self.element.innerHTML = emicsection.svg_document(draw_bboxes = draw_bboxes).toxml()

class XMLCanvas(Canvas):
  """Creates an XML element as a Canvas, which we write an SVG inside."""

  def __init__(self, element):
    # element should be an XML minidom element
    self.element = element
  
  def render(self, emicsection, draw_bboxes = False):
    # FIXME: replace instead of appending
    self.element.appendChild(emicsection.svg_document(draw_bboxes = draw_bboxes).childNodes[0])
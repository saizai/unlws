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
    pass
  
  def render(self, emicsection):
    self.element.innerHTML = emicsection.svg_document().toxml()

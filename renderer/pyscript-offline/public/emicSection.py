from copy import deepcopy
import math
import xml.dom.minidom as minidom
import svgpathtools
from BPHaver import BPHaver

class EmicSection(BPHaver):
  """A section within an UNLWS text, containing subsections and rels between them."""
  # TODO: use this class as a middleman to handle multiple rels connected to the same BP.

  def __init__(self):
    """Initialise this Section to have a position and rotation."""
    super().__init__()

    self.subsections = [] # subsections in the section
    self.rels = [] # rels in the section

    # Position in the supersection, in svg-style coordinates where
    # x increases right and y increases down.
    self._x = 0.
    self._y = 0.
    # Angle of rotation of the section, in *radians*.  0 is rightward.
    # A positive angle is a clockwise rotation, to match the reflected y.
    self._angle = 0.
  
  @classmethod
  def from_glyph(self, glyph):
    return SingleGlyphEmicSection(glyph)
  
  @property
  def x(self):
    return self._x
  @x.setter
  def x(self, value):
    self._x = value
  @property
  def y(self):
    return self._y
  @y.setter
  def y(self, value):
    self._y = value
  @property
  def angle(self):
    return self._angle
  @angle.setter
  def angle(self, value):
    self._angle = value

  @property
  def angle_in_degrees(self):
    "Rotation of this section in degrees."
    return self.angle*180./math.pi
  
  @property
  def z(self):
    "Translation of this section as a complex number."
    return self.x+self.y*(0+1j)
  
  
  def add_subsection(self, subsec):
    "Add the EmicSection subsec to this section's list of subsections."
    self.subsections.append(subsec)
  
  def add_rel(self, rel):
    self.rels.append(rel)

  
  
  # def svgpathtools_paths(self):
  #   """Return a list of svgpathtools Path objects represented by this section.
    
  #   The Path objects returned are in global svg coordinates."""
  #   # Code patterned on the svg2paths function in svgpathtools.
  #   # That has a file read baked in which means we can't use it directly.
  #   # TODO: we may want to keep the attributes.
  #   def dom2dict(element):
  #       """Converts DOM elements to dictionaries of attributes."""
  #       keys = list(element.attributes.keys())
  #       values = [val.value for val in list(element.attributes.values())]
  #       return dict(list(zip(keys, values)))
    
  #   d_strings = [el.getAttribute('d')
  #       for el in self.lemma_svg.getElementsByTagName('path')]
  #   d_strings += [svgpathtools.polyline2pathd(dom2dict(el))
  #       for el in self.lemma_svg.getElementsByTagName('polyline')]
  #   d_strings += [svgpathtools.polygon2pathd(dom2dict(el))
  #       for el in self.lemma_svg.getElementsByTagName('polygon')]
  #   d_strings += [('M' + l.getAttribute('x1') + ' ' + l.getAttribute('y1') +
  #                  'L' + l.getAttribute('x2') + ' ' + l.getAttribute('y2'))
  #       for el in self.lemma_svg.getElementsByTagName('line')]
  #   d_strings += [svgpathtools.ellipse2pathd(dom2dict(el))
  #       for el in self.lemma_svg.getElementsByTagName('ellipse')]
  #   d_strings += [svgpathtools.ellipse2pathd(dom2dict(el))
  #       for el in self.lemma_svg.getElementsByTagName('circle')]
  #   d_strings += [svgpathtools.rect2pathd(dom2dict(el))
  #       for el in self.lemma_svg.getElementsByTagName('rect')]
    
  #   path_list = [svgpathtools.parse_path(d) for d in d_strings]
  #   return [p.rotated(self.angle_in_degrees, origin=0+0j).translated(self.z)
  #       for p in path_list]
  
  def bounding_box(self, stroke_width_allowance = 0.):
    """Return the bounding box for this section, as a 4-tuple
    (xmin, xmax, ymin, ymax).
    
    Arguments:
    stroke_width_allowance: pad the bounding box by this much on each side,
      to allow for stroke width"""
    subsection_bboxes = [p.bounding_box(0.) for p in self.subsections]
    sbox = (
            min(b[0] for b in subsection_bboxes),
            max(b[1] for b in subsection_bboxes),
            min(b[2] for b in subsection_bboxes),
            max(b[3] for b in subsection_bboxes),
            )
    return (
            sbox[0]-stroke_width_allowance,
            sbox[1]+stroke_width_allowance,
            sbox[2]-stroke_width_allowance,
            sbox[3]+stroke_width_allowance,
            )
  
  def svg(self):
    """Return an SVG of this sentence as XML."""
    svg = minidom.getDOMImplementation().createDocument("http://www.w3.org/2000/svg", "svg", None)
    svg.documentElement.setAttribute("xmlns", "http://www.w3.org/2000/svg")
    svg.documentElement.setAttribute("xmlns:unlws-renderer", "https://github.com/saizai/unlws")
    bbox = self.bounding_box()
    svg.documentElement.setAttribute("viewBox", f"{bbox[0]} {bbox[2]} {bbox[1]-bbox[0]} {bbox[3]-bbox[2]}")
    # for now, magic scaling of 32px per UNLWS em
    svg.documentElement.setAttribute("width", str(int(32*(bbox[1]-bbox[0])))+"px")

    svg.documentElement.appendChild(self.style)
    
    for subsection in self.subsections:
      ## test: show bounding box
      #bbox = glyph.bounding_box(stroke_width_allowance=self.default_stroke_width)
      #r = svg.createElement("rect")
      #r.setAttribute("x", str(bbox[0]))
      #r.setAttribute("width", str(bbox[1]-bbox[0]))
      #r.setAttribute("y", str(bbox[2]))
      #r.setAttribute("height", str(bbox[3]-bbox[2]))
      #r.setAttribute("fill", "none")
      #r.setAttribute("stroke", "green")
      #r.setAttribute("stroke-width", str(1./36))
      #svg.documentElement.appendChild(r)
      el = subsection.svg()
      el.setAttribute("class", self.text_class)
      svg.documentElement.appendChild(el)
    for rel in self.rels:
      ## test: show bounding box
      #bbox = rel.bounding_box(stroke_width_allowance=self.default_stroke_width)
      #r = svg.createElement("rect")
      #r.setAttribute("x", str(bbox[0]))
      #r.setAttribute("width", str(bbox[1]-bbox[0]))
      #r.setAttribute("y", str(bbox[2]))
      #r.setAttribute("height", str(bbox[3]-bbox[2]))
      #r.setAttribute("fill", "none")
      #r.setAttribute("stroke", "red")
      #r.setAttribute("stroke-width", str(1./36))
      #svg.documentElement.appendChild(r)
      el = rel.svg()
      el.setAttribute("class", self.text_class)
      svg.documentElement.appendChild(el)
    
    return svg

class SingleGlyphEmicSection(EmicSection):
  """An instance of a glyph within a text."""

  def __init__(self, glyph=None):
    super().__init__()
    self.glyph = glyph
    # self.add_subsection(glyph) # TODO: Do I want this? Probably not, since Glyphs don't work like EmicSections
  
  @property
  def lemma_svg(self):
    return self.glyph.lemma_svg
    # TODO: this method may be unnecessary and confusing

  def svg(self, drawBPs = False):
    """Return a rendered SVG, with the correct coordinate transform.
    
    If `drawBPs` is true, draw the BPs as green circles."""
    surface_svg = deepcopy(self.lemma_svg)
    surface_svg.setAttribute("transform", f"translate({self.x} {self.y}) rotate({self.angle_in_degrees})")
    
    if drawBPs:
      # Again create a document, urgh.
      document = minidom.getDOMImplementation().createDocument("http://www.w3.org/2000/svg", "svg", None)
      for bp in self._lemma_bps.values():
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

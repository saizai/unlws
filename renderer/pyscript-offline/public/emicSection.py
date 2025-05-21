import re
from copy import deepcopy
import math
import xml.dom.minidom as minidom
import svgpathtools
from BPHaver import BPHaver

class EmicSection(BPHaver):
  """An UNLWS sentence, with the layout of how it sits on the page, containing subsections and rels between them."""
  # TODO: use this class as a middleman to handle multiple rels connected to the same BP.

  def __init__(self, dictionary = None, name = None):
    """Initialise this Section to have a position, rotation, name, subsections and rels."""
    if not name: name = "sec_" + hex(id(object))
    self.name = name

    super().__init__()

    if dictionary: # FIXME: this is a hack for DifferentialSectionFromEmic, which doesn't pass the dictionary parameter.
      self.dictionary = dictionary
      # FIXME: style does not belong in the dictionary
      self.style = dictionary.style
      # default SVG class for UNLWS text, to be used with the style
      self.text_class = dictionary.text_class
    
    self.color = None

    self.subsections = [] # subsections in the section
    self.rels = [] # rels in the section

    # Position in the supersection, in svg-style coordinates where
    # x increases right and y increases down.
    self.x = 0.
    self.y = 0.
    # Angle of rotation of the section, in *radians*.  0 is rightward.
    # A positive angle is a clockwise rotation, to match the reflected y.
    self.angle = 0.
  
  @classmethod
  def from_glyph(self, glyph, dictionary, name = None):
    return SingleGlyphEmicSection(glyph, dictionary = dictionary, name = name)

  @property
  def angle_in_degrees(self):
    "Rotation of this section in degrees."
    return self.angle*180./math.pi
  
  @property
  def z(self):
    "Translation of this section as a complex number."
    return self.x+self.y*(0+1j)
  
  @property
  def default_stroke_width(self):
    "The default stroke width according to the style of this text."
    # FIXME: this is a crude and brittle inspection of the CSS. Do better.
    # E.g. look for self.text_class as a selector.
    css = self.style.childNodes[0].data
    span = re.search('stroke-width\\s*:\\s*([-+0-9.eE]*)', css).span(1)
    return float(css[span[0]:span[1]])


  def add_subsection(self, subsec, bp_renaming=None):
    "Add the EmicSection subsec to this section's list of subsections."
    self.subsections.append(subsec)
    # TODO: implement bp_renaming to mark what BPs this section should pass forward from its subsections.
    # Default (==None?) would be for this section to have all BPs that any subsections have, and to use the same names for them. But it should be possible to only pass some of the BPs and to rename them.
    # For example, `bp_renaming = {"X": "A", "Y": ""}` would mean that this section gets two new BPs (A and Y) which correspond to `subsec`'s BPs (X and Y respectively). Any other BPs of `subsec` are not passed along. `bp_renaming = {}` would mean no BPs are passed along.
  
  def add_rel(self, rel):
    self.rels.append(rel)


  def bp(self, name):
    """Return the BP `name`, in sentence coordinates with transformation applied."""
    return self.lemma_bps[name].rotate(self.angle).translate(self.x, self.y)
  
  def parent_coords_to_own(self, x, y):
    """Return (x, y) from the parent's coordinate system transformed to this BPHaver's own coordinate system."""
    xnew, ynew = x-self.x, y-self.y
    c, s = math.cos(-self.angle), math.sin(-self.angle)
    xnew = c*xnew - s*ynew
    ynew = s*xnew + c*ynew
    return xnew, ynew
  
  
  # def svgpathtools_paths(self):
  #   """Return a list of svgpathtools Path objects represented by this section.
    
  #   The Path objects returned are in the parent section's coordinates."""
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
  
  def bounding_box(self, stroke_width_allowance = 0., own_coords = False):
    """Return the bounding box for this section, as a 4-tuple
    (xmin, xmax, ymin, ymax).
    
    Arguments:
    stroke_width_allowance: pad the bounding box by this much on each side,
      to allow for stroke width"""
    
    # Temporary solution for the below fixme
    r = self.bounding_disk_radius()
    return (-r, r, -r, r)

    # FIXME: this doesn't work when the section is transformed.
    subsection_bboxes = [p.bounding_box(0., own_coords = own_coords) for p in self.subsections]

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
  
  def bounding_disk_radius(self):
    """Gives the radius of a disk centered at (0, 0) that contains the bounding disks of its subsections."""

    return max(math.sqrt(subsec.x**2+subsec.y**2) + subsec.bounding_disk_radius() for subsec in self.subsections)
  

  def svg_bounding_box(self, color = "red", own_coords = False):
    # """Return a `<rect>` element that bounds this section."""
    # svg = minidom.getDOMImplementation().createDocument("http://www.w3.org/2000/svg", "svg", None)
    # bbox = self.bounding_box(stroke_width_allowance=self.default_stroke_width)
    # r = svg.createElement("rect")
    # r.setAttribute("x", str(bbox[0]))
    # r.setAttribute("width", str(bbox[1]-bbox[0]))
    # r.setAttribute("y", str(bbox[2]))
    # r.setAttribute("height", str(bbox[3]-bbox[2]))
    # r.setAttribute("fill", "none")
    # r.setAttribute("stroke", color)
    # r.setAttribute("stroke-width", str(1./36))
    # return r
    """Return a `<circle>` element that bounds this section."""
    svg = minidom.getDOMImplementation().createDocument("http://www.w3.org/2000/svg", "svg", None)
    c = svg.createElement("circle")
    c.setAttribute("cx", str(self.x))
    c.setAttribute("cy", str(self.y))
    c.setAttribute("r", str(self.bounding_disk_radius()))
    c.setAttribute("fill", "none")
    c.setAttribute("stroke", color)
    c.setAttribute("stroke-width", str(1./36))
    return c

  def svg(self, **kwargs):
    """Return this section as an XML `<g>` element.
    
    kwargs:
    * if `draw_BPs` is true, draw the BPs as green circles;
    * if `draw_bboxes` is true, draw rectangles around rel lines and circles around sections."""
    document = minidom.getDOMImplementation().createDocument("http://www.w3.org/2000/svg", "svg", None)
    g = document.createElement("g")
    if self.color:
      g.setAttribute("stroke", self.color)
    g.setAttribute("transform", f"translate({self.x} {self.y}) rotate({self.angle_in_degrees})")
          
    for subsection in self.subsections:
      if kwargs.get("draw_bboxes", False):
        r = subsection.svg_bounding_box()
        g.appendChild(r)

      el = subsection.svg(**kwargs)
      # el.setAttribute("class", self.text_class)
      g.appendChild(el)
    
    for rel in self.rels:
      if kwargs.get("draw_bboxes", False):
        r = rel.svg_bounding_box(color = "green")
        g.appendChild(r)
      
      el = rel.svg()
      # el.setAttribute("class", self.text_class)
      g.appendChild(el)
    
    return g

  def svg_document(self, **kwargs):
    """Return an SVG of this section as XML.
    
    kwargs:
    * if `draw_BPs` is true, draw the BPs as green circles;
    * if `draw_bboxes` is true, draw rectangles around rel lines and circles around sections."""
    svg = minidom.getDOMImplementation().createDocument("http://www.w3.org/2000/svg", "svg", None)
    document = svg.documentElement
    
    document.setAttribute("xmlns", "http://www.w3.org/2000/svg")
    document.setAttribute("xmlns:unlws-renderer", "https://github.com/saizai/unlws")
    bbox = self.bounding_box(stroke_width_allowance = 5 * self.default_stroke_width)
    document.setAttribute("viewBox", f"{bbox[0]} {bbox[2]} {bbox[1]-bbox[0]} {bbox[3]-bbox[2]}")
    # for now, magic scaling of 32px per UNLWS em
    document.setAttribute("width", str(int(32*(bbox[1]-bbox[0])))+"px")

    document.appendChild(self.style)
    
    contents = self.svg(**kwargs)
    contents.setAttribute("class", self.text_class)
    document.appendChild(contents)
    
    return svg

  def __repr__(self):
    res = f"{type(self).__name__} \"{self.name}\" ("
    for subsec in self.subsections:
      res += subsec.name
    res += ")"
    return res

class SingleGlyphEmicSection(EmicSection):
  """An instance of a glyph within a text."""

  def __init__(self, glyph = None, dictionary = None, name = None):
    super().__init__(dictionary = dictionary, name = name)
    self.glyph = glyph
    # self.add_subsection(glyph) # TODO: Do I want this? Probably not, since Glyphs don't work like EmicSections
  
  @property
  def lemma_svg(self):
    return self.glyph.lemma_svg
    # TODO: this method may be unnecessary and confusing

  def svg(self, **kwargs):
    """Return a rendered SVG, with the correct coordinate transform.
    
    kwargs:
    * if `draw_BPs` is true, draw the BPs as green circles."""
    surface_svg = deepcopy(self.lemma_svg)
    surface_svg.setAttribute("transform", f"translate({self.x} {self.y}) rotate({self.angle_in_degrees})")
    
    if kwargs.get("draw_BPs", False):
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
  
  def svgpathtools_paths(self, own_coords = False):
    """Return a list of svgpathtools Path objects represented by this glyph.
    
    The Path objects returned are in the parent section's coordinates, unless own_coords is set to True."""
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
    d_strings += [('M' + el.getAttribute('x1') + ' ' + el.getAttribute('y1') +
                   'L' + el.getAttribute('x2') + ' ' + el.getAttribute('y2'))
        for el in self.lemma_svg.getElementsByTagName('line')]
    d_strings += [svgpathtools.ellipse2pathd(dom2dict(el))
        for el in self.lemma_svg.getElementsByTagName('ellipse')]
    d_strings += [svgpathtools.ellipse2pathd(dom2dict(el))
        for el in self.lemma_svg.getElementsByTagName('circle')]
    d_strings += [svgpathtools.rect2pathd(dom2dict(el))
        for el in self.lemma_svg.getElementsByTagName('rect')]
    
    path_list = [svgpathtools.parse_path(d) for d in d_strings]
    if own_coords:
      return path_list
    else:
      return [p.rotated(self.angle_in_degrees, origin=0+0j).translated(self.z)
        for p in path_list]
  
  def bounding_box(self, stroke_width_allowance = 0., own_coords = False):
    """Return the bounding box for this glyph, as a 4-tuple
    (xmin, xmax, ymin, ymax).
    
    Arguments:
    stroke_width_allowance: pad the bounding box by this much on each side,
      to allow for stroke width"""
    path_bboxes = [p.bbox() for p in self.svgpathtools_paths(own_coords = own_coords)]
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

  def bounding_disk_radius(self):
    xmin, xmax, ymin, ymax = self.bounding_box(own_coords = True) # FIXME: take into account stroke width
    distance_to_vertical_edge = max(abs(xmin), abs(xmax))
    distance_to_horizontal_edge = max(abs(ymin), abs(ymax))
    distance_to_farthest_corner = math.sqrt(distance_to_vertical_edge**2 + distance_to_horizontal_edge**2)
    return distance_to_farthest_corner

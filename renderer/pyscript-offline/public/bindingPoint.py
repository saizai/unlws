from copy import copy
import math

class BindingPoint:
  """An instance of a binding point, either within a glyph or a larger text.
  
  Properties:
  x, y: coordinates relative to the host
  handlex, handley: ditto for the spline handle
  host: the glyph this BP belongs to
  name: the name of this BP within `host`"""
  def __init__(self, x = 0., y = 0., handlex = None, handley = None,
      angle = None, speed = 1.):
    """Arguments:
    x, y: coordinates in svg conventions
    handlex, handley: coordinates of the spline handle
    angle: angle in radians, 0 is rightward, positive is clockwise
    speed: distance between the BP itself and its handle, default 1
    
    Either handle coordinates or angle ought to be provided."""
    self.x = x
    self.y = y
    if handlex != None and handley != None:
      self.handlex = handlex
      self.handley = handley
    else:
      if angle == None: angle = 0. # some default
      self.handlex = x + speed * math.cos(angle)
      self.handley = y + speed * math.sin(angle)
  
  # For svgpathtools, which represents points as complex numbers.
  @property
  def z(self):
    "Position of this BP as a complex number."
    return self.x+self.y*(0+1j)
  
  @property
  def handlez(self):
    "Position of this BP's spline handle as a complex number."
    return self.handlex+self.handley*(0+1j)
  
  def translate(self, dx, dy):
    """Return a copy of this BP translated by (dx, dy)."""
    p = copy(self)
    p.x += dx
    p.y += dy
    p.handlex += dx
    p.handley += dy
    return p
  
  def rotate(self, dangle):
    """Return a copy of this BP rotated around the origin by dangle."""
    c, s = math.cos(dangle), math.sin(dangle)
    p = copy(self)
    p.x = c*self.x - s*self.y
    p.y = s*self.x + c*self.y
    p.handlex = c*self.handlex - s*self.handley
    p.handley = s*self.handlex + c*self.handley
    return p


class RelativeBindingPoint(BindingPoint):
  """A simulation of a BP. It gives the coordinates as if the BP was a BP of `sub_host`'s sibling, when it is actually a BP of sub_host."""
  def __init__(self, sub_host, sub_bp_name):
    self.sub_bp_name = sub_bp_name
    self.sub_host = sub_host

  @property
  def sub_bp(self):
    return self.sub_host.bp(self.sub_bp_name)
  
  @property
  def x(self):
    return self.sub_bp.x
  @property
  def y(self):
    return self.sub_bp.y
  @property
  def handlex(self):
    return self.sub_bp.handlex
  @property
  def handley(self):
    return self.sub_bp.handley
  
  def set_position(self, x, y):
    self.x, self.y = self.sub_host.parent_coords_to_own(x, y)
  def set_handles(self, handlex, handley):
    self.handlex, self.handley = self.sub_host.parent_coords_to_own(handlex, handley)
  
  def translate(self, dx, dy):
    x = self.x + dx
    y = self.y + dy
    handlex = self.handlex + dx
    handley = self.handley + dy
    # self.set_position(x, y)
    # self.set_handles(handlex, handley)
    p = BindingPoint(x, y, handlex, handley)
    return p

  def rotate(self, dangle):
    c, s = math.cos(dangle), math.sin(dangle)
    x = c*self.x - s*self.y
    y = s*self.x + c*self.y
    handlex = c*self.handlex - s*self.handley
    handley = s*self.handlex + c*self.handley
    # self.set_position(x, y)
    # self.set_handles(handlex, handley)
    p = BindingPoint(x, y, handlex, handley)
    return p
import numpy, svgpathtools
from bindingPoint import BindingPoint
from glyph import Glyph
from relLine import RelLine

# Apparatus for computing derivatives for gradient descent.

class DifferentialBindingPoint(BindingPoint):
  "An instance of a binding point with derivatives of position."

  # For now with fewer arguments because we'll probably never create
  def __init__(self, x = 0., y = 0., handlex = 0., handley = 0.):
    super().__init__(x=x, y=y, handlex=handlex, handley=handley)
    self.dx = 0.
    self.dy = 0.
    self.handledx = 0.
    self.handledy = 0.

  @property
  def dz(self):
    "Differential of position of this BP as a complex number."
    return self.dx+self.dy*(0+1j)

  @property
  def handledz(self):
    "Differential of position of this BP's spline handle as a complex number."
    return self.handledx+self.handledy*(0+1j)

  def translate(self, delta_x, delta_y):
    p = super().translate(delta_x, delta_y)
    diff_p = DifferentialBindingPoint(p.x, p.y, p.handlex, p.handley)
    diff_p.dx += delta_x
    diff_p.dy += delta_y
    diff_p.handledx += delta_x
    diff_p.handledy += delta_y
    return diff_p

  def rotate(self, delta_angle):
    c, s = math.cos(delta_angle), math.sin(delta_angle)
    p = super().rotate(delta_angle)
    diff_p = DifferentialBindingPoint(p.x, p.y, p.handlex, p.handley)
    diff_p.dx = c*self.dx - s*self.dy
    diff_p.dy = s*self.dx + c*self.dy
    diff_p.handledx = c*self.handledx - s*self.handledy
    diff_p.handledy = s*self.handledx + c*self.handledy
    return diff_p

class DifferentialGlyph(Glyph):
  "An instance of a glyph with derivatives of position and rotation."

  def __init__(self, lemma_svg = None):
    """Initialise this glyph."""
    super().__init__(lemma_svg)
    # Derivatives of our position and angle statistics.
    self.dx = 0.
    self.dy = 0.
    self.dangle = 0.
  
  @classmethod
  def from_glyph(self, g):
    "Return glyph g upgraded to a DifferentialGlyph."
    dg = DifferentialGlyph(g.lemma_svg)
    dg.x = g.x
    dg.y = g.y
    dg.angle = g.angle
    dg.lemma_bps = g.lemma_bps
    return dg
  
  @property
  def dangle_in_degrees(self):
    "Differential of rotation of this glyph in degrees."
    return self.dangle*180./math.pi
  
  @property
  def dz(self):
    "Differential of translation of this glyph as a complex number."
    return self.dx+self.dy*(0+1j)
  
  def bp(self, name):
    "Return the differential BP `name`, with transformation applied."
    q = self.lemma_bps[name].rotate(self.angle)
    p = q.translate(self.x, self.y)
    diff_p = DifferentialBindingPoint(p.x, p.y, p.handlex, p.handley)
    diff_p.dx = self.dx - self.dangle * q.y
    diff_p.dy = self.dy + self.dangle * q.x
    diff_p.handledx = self.dx - self.dangle * q.handley
    diff_p.handledy = self.dy + self.dangle * q.handlex
    return diff_p

def dpoly(rel):
  """Return the numpy.poly1d of the first-order derivative 
  in the gradient-descent variable of the parametrised curve."""
  bezier = svgpathtools.CubicBezier(rel.bp0.dz, rel.bp0.handledz, rel.bp1.handledz, rel.bp1.dz)
  return bezier.poly()



# The particular penalties below are not necessarily the ones we'll want to
# go with in the end.

def velocity_penalty(rel):
  "Penalty for this rel not going at constant velocity."
  bezier = rel.svgpathtools_bezier()
  dd = bezier.poly().deriv().deriv()
  ddx = [float(dd[i].real) for i in range(0,2)]
  ddy = [float(dd[i].imag) for i in range(0,2)]
  # This is the integral of ddx(t)^2 + ddy(t)^2 for t from 0 to 1.
  return (ddx[1]*ddx[1]+ddy[1]*ddy[1])/3 +\
    ddx[0]*ddx[1]+ddy[0]*ddy[1] +\
    ddx[0]*ddx[0]+ddy[0]*ddy[0]

def deriv_velocity_penalty(rel):
  """Derivative of penalty for this rel not going at constant velocity.
  
  The glyphs which rel is attached to should be DifferentialGlyph objects."""
  bezier = rel.svgpathtools_bezier()
  dd = bezier.poly().deriv().deriv()
  ddx = [float(dd[i].real) for i in range(0,2)]
  ddy = [float(dd[i].imag) for i in range(0,2)]
  du_dd = dpoly(rel).deriv().deriv()
  du_ddx = [float(du_dd[i].real) for i in range(0,2)]
  du_ddy = [float(du_dd[i].imag) for i in range(0,2)]
  # This is the integral of d/du of ddx(t)^2 + ddy(t)^2 for t from 0 to 1,
  # where u is the gradient descent variable.
  return 2*(ddx[1]*du_ddx[1]+ddy[1]*du_ddy[1])/3 +\
    ddx[0]*du_ddx[1]+ddy[0]*du_ddy[1] +\
    du_ddx[0]*ddx[1]+du_ddy[0]*ddy[1] +\
    2*(ddx[0]*du_ddx[0]+ddy[0]*du_ddy[0])

def curvature_penalty(rel):
  "Maximum unsigned curvature attained at any point of this rel."
  return _curvature_penalty(rel, False)

def deriv_curvature_penalty(rel):
  "Derivative of maximum unsigned curvature attained."
  return _curvature_penalty(rel, True)

def _curvature_penalty(rel, differentiate):
  """Computations for maximum curvature on this rel.
  
  Parameters:
  differentiate: boolean, whether to return the derivative."""
  # Let x, y be the coordinates of the cubic curve.
  # Let ' denote derivative in the parameter of the curve (which we call t).
  # Signed curvature is k = (x'y'' - y'x'')/((x'^2+y^'2)^(3/2)).
  # k' = [ (x''y''+x'y'''-y''x''-y'x''')(x'^2+y^'2)^(3/2)
  # - (x'y''-y'x'')*3/2(x'^2+y'^2)^(1/2)*2(x'x''+y'y'') ]
  # / ((x^2+y^2)^3)
  # = [ (x'y'''-y'x''')(x'^2+y^'2) - (x'y''-y'x'')*3(x'x''+y'y'') ]
  # / ((x^2+y^2)^(5/2))).
  # For a cubic curve the degree of the numerator is generically 5
  # because of cancellations in the leading coefficient.
  bezier = rel.svgpathtools_bezier()
  d = bezier.poly().deriv()
  dx = numpy.poly1d([float(c.real) for c in d.c])
  dy = numpy.poly1d([float(c.imag) for c in d.c])
  ddx = dx.deriv()
  ddy = dy.deriv()
  dddx = ddx.deriv()
  dddy = ddy.deriv()
  
  def curvature(t):
    "Evaluation of the signed curvature at curve parameter t."
    dxt = dx(t)
    dyt = dy(t)
    return (dxt*ddy(t)-dyt*ddx(t)) / pow(dxt*dxt+dyt*dyt, 1.5)
  
  # numerator of k'
  ndk = numpy.polysub(numpy.polymul(
      numpy.polysub(numpy.polymul(dx, dddy), numpy.polymul(dy, dddx)),
      numpy.polyadd(numpy.polymul(dx, dx), numpy.polymul(dy, dy)) ),
    numpy.polymul(
      numpy.polysub(numpy.polymul(dx, ddy), numpy.polymul(dy, ddx)),
      numpy.polyadd(numpy.polymul(dx, ddx), numpy.polymul(dy, ddy)) )*3.
    )
  criticals = numpy.roots(ndk)
  criticals = [0., 1.] + [t.real for t in criticals if t.imag==0. and t.real >= 0. and t.real <= 1.]
  k_at_criticals = [curvature(t) for t in criticals]
  abs_kmax, tmax, imax = max((abs(k_at_criticals[i]),criticals[i],i) for i in range(len(criticals)))
  if not differentiate:
    return abs_kmax
  
  sign_max = -1. if k_at_criticals[imax] < 0. else 1.
  
  du_d = dpoly(rel).deriv()
  du_dx = numpy.poly1d([float(c.real) for c in du_d.c])
  du_dy = numpy.poly1d([float(c.imag) for c in du_d.c])
  du_ddx = du_dx.deriv()
  du_ddy = du_dy.deriv()
  
  dxt = dx(tmax)
  dyt = dy(tmax)
  ddxt = ddx(tmax)
  ddyt = ddy(tmax)
  du_dxt = du_dx(tmax)
  du_dyt = du_dy(tmax)
  du_ddxt = du_ddx(tmax)
  du_ddyt = du_ddy(tmax)
  
  # If the maximum curvature is attained at an endpoint,
  # we just want the u-derivative of curvature there.
  # The evaluations du_dxt, etc. above are correct for this purpose.
  #
  # But if the maximum curvature is attained at an interior critical point tmax,
  # work out a=dt/du on the locus of critical points by implicit differentiation,
  # and then differentiate the max curvature not in direction du but du+a dt.
  if imax >= 2:
    dddxt = dddx(tmax)
    dddyt = dddy(tmax)
    du_dddx = du_ddx.deriv()
    du_dddy = du_ddy.deriv()
    du_dddxt = du_dddx(tmax)
    du_dddyt = du_dddy(tmax)
    # Consider p = ndk(t) + u du_ndk(t) and find (dp/du)/(dp/dt)
    # at (t, u) = (tmax, 0).
    dp = ndk.deriv()(tmax) # ndk.deriv() = (dp/dt)|u=0
    # And below is dp/du, which is independent of u, at tmax.
    # recall, ndk = (x'y'''-y'x''')(x'^2+y^'2) - (x'y''-y'x'')*3(x'x''+y'y'')
    du_p = (du_dxt*dddyt+dxt*du_dddyt-du_dyt*dddxt-dyt*du_dddxt)*(dxt*dxt+dyt*dyt) + \
      2*(dxt*dddyt-dyt*dddxt)*(du_dxt*dxt+du_dyt*dyt) - \
      3*(du_dxt*ddyt+dxt*du_ddyt-du_dyt*ddxt-dyt*du_ddxt)*(dxt*ddxt+dyt*ddyt) - \
      3*(dxt*ddyt-dyt*ddxt)*(du_dxt*ddxt+dxt*du_ddxt+du_dyt*ddyt+dyt*du_ddyt)
    a = du_p/dp
    # Replace the four du_ variables used below by derivatives in direction du+a dt.
    du_dxt += a*ddxt
    du_dyt += a*ddyt
    du_ddxt += a*dddxt
    du_ddyt += a*dddyt
  
  du_k = ((du_dxt*ddyt+dxt*du_ddyt-du_dyt*ddxt-dyt*du_ddxt)*(dxt*dxt+dyt*dyt) - \
    3*(dxt*ddyt-dyt*ddxt)*(du_dxt*dxt+du_dyt*dyt)) / \
    pow(dxt*dxt+dyt*dyt, 2.5)
  return sign_max * du_k

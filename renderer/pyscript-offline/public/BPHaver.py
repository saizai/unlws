from bindingPoint import BindingPoint

class BPHaver():
  """Any object that has binding points. Allows BPs to be added and read."""
  def __init__(self):
    # Binding points, as a hash from name to BP object.
    # Stored in the coordinates of the lemma form, rather than as transformed.
    self.lemma_bps = {}
  
  def addBP(self, name, bp):
    """Add `bp` with the name `name`."""
    bp.host = self
    bp.name = name
    self.lemma_bps[name] = bp
  
  def bp(self, name):
    """Return the BP `name`, in sentence coordinates with transformation applied."""
    return self.lemma_bps[name].rotate(self.angle).translate(self.x, self.y)
  
  def copy_BPs_from(self, source):
    for bp in source.lemma_bps.values():
      self.addBP(bp.name, bp)

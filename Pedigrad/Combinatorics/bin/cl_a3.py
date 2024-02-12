class A3(object):

  def __init__(self,up,down,plane):
    self.plane = plane
    self.up = 0 if self.plane == 0 else up
    self.down = 0 if self.plane == 0 else down

  def __str__(self):
    if self.up == 1 and self.down == 0:
      return u"\u21d1"
    if self.up == 0 and self.down == 1:
      return 	u"\u21d3"
    if self.up == 1 and self.down == 1:
      return u"\u21d5"
    if self.up == 0 and self.down == 0 and self.plane != 0:
      return "O"
    if self.plane == 0:
      return "e"

  def __eq__(self,element):
    return (self.plane == element.plane) and (self.up == element.up) and (self.down == element.down)

  def __ne__(self,element):
    return not(self == element)

  def __lt__(self,element):
    return (self.plane < element.plane) or (self.plane == element.plane and self.up <= element.up and self.down < element.down) or (self.plane == element.plane and self.up < element.up and self.down <= element.down)

  def __add__(self,element):
    return A3(self.up | element.up, self.down | element.down, self.plane | element.plane)

  def __mul__(self,element):
    if self != A3(1,1,1):
      return A3(0,0,0) if (element != self) and (element != A3(1,1,1)) else self
    else:
      return element

  def __contains__(self,z3_elt):
    if self.plane == 1:
      z = z3_elt + Z3(self.up,self.down)
      return (z == Z3(0,0)) or (z == Z3(1,1))
    else:
      return (z3_elt == Z3(1,1))
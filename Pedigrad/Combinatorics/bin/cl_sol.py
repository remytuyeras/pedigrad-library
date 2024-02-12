class Z3sol(object):

  def __init__(self,z3_elt):
    self.z3_elt = z3_elt
    self.a3_elt = A3(z3_elt.down,z3_elt.up,1)

  def __str__(self):
    return sol_symb(str(self.z3_elt))

  def __contains__(self,z3_elt):
    return z3_elt in self.a3_elt

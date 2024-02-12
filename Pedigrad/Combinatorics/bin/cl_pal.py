class A3polynomial(object):

  def __init__(self,*monomials):
    self.monomials = sorted(monomials)

  def __str__(self):
    if self.monomials == []:
      return str(A3(0,0,0))
    else:
      s = ""
      for i in range(len(self.monomials)):
        if not( self.monomials[i] in [A3monomial([]),A3monomial()] ):
          s = s + spc_sum_symb(s,"*") + str(self.monomials[i])
      return s

  def __add__(self,monomial):
    return A3polynomial(*(self.monomials + monomial.monomials))
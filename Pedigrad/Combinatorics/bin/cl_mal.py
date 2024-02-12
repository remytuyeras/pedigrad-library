class A3monomial(object):

  def __init__(self,*var_lists):
    self.var_lists = sorted(map(sorted,var_lists))

  def __str__(self):
    if self.var_lists == []:
      return str(A3(0,0,0))
    else:
      s = ""
      for i in range(len(self.var_lists)):
        s_var_list = ""
        if self.var_lists[i] == []:
          s_var_list = str(A3(0,0,1))
        else:
          for j in range(len(self.var_lists[i])):
            s_var_list = s_var_list + sum_symb(s_var_list,"*") + "z"+str(self.var_lists[i][j])
          s_var_list = sol_symb(s_var_list)
        s = s + cap_symb(s,s_var_list) + s_var_list
      return s

  def __eq__(self,element):
    return self.var_lists == element.var_lists

  def __ne__(self,element):
    return not(self == element)

  def __lt__(self,element):
    return self.var_lists < element.var_lists

  def __mul__(self,monomial):
    #To handle the absorbtion by e = ()
    if self.var_lists == () or monomial.var_lists == ():
      return A3monomial()
    return A3monomial(*(self.var_lists + monomial.var_lists))
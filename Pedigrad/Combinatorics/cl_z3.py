from __future__ import annotations

class Z3(object):

  __slots__ = ("up","down")

  def __init__(self,
               #List of inputs and their types
               up: int,
               down: int
               #The output type
               ) -> None:
    """
    Encodes an element of the semring strucutre \overline{\mathbb{Z}}_3 as a pair of 
    Boolean value (see documentation).
    """
    self.up = up
    self.down = down

  def __str__(self) -> str:
    """
    Displays the graphic representation of a Z3 instance as an double directed arrow or a dot
    for the zero element.
    """
    if self.up == 1 and self.down == 0:
      return u"\u2191"
    if self.up == 0 and self.down == 1:
      return 	u"\u2193"
    if self.up == 1 and self.down == 1:
      return u"\u2195"
    if self.up == 0 and self.down == 0:
      return u"\u00B7"

  def __eq__(self,
             #List of inputs and their types
             element: Z3
             #The output type
             ) -> bool:
    """
    Tests a componentwise equality test for Z3 instances.
    """
    return (self.up == element.up) and (self.down == element.down)

  def __ne__(self,
             #List of inputs and their types
             element: Z3
             #The output type
             ) -> bool:
    """
    Tests a componentwise inequality test for Z3 instances.
    """
    return not(self == element)

  def __lt__(self,
             #List of inputs and their types
             element: Z3
             #The output type
             ) -> bool:
    """
    Tests a componentwise comparison test for Z3 instances using the "less than" pre-order
    relation.
    """
    return (self.up <= element.up and self.down < element.down) or (self.up < element.up and self.down <= element.down)

  def __add__(self,
              #List of inputs and their types
              element: Z3
              #The output type
              ) -> Z3:
    """
    Implements the addition operation associated with the semiring structure.
    """
    return Z3(self.up | element.up, self.down | element.down)

  def __mul__(self,
              #List of inputs and their types
              element: Z3
              #The output type
              ) -> Z3:
    """
    Implements the multiplication operation associated with the semiring structure.
    """
    return Z3((self.up & element.up) | (self.down & element.down), (self.down & element.up) | (self.up & element.down))

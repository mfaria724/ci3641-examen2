import itertools
from Atom import Atom

# se que en este modulo hay un monton de código repetido pero no tenía demasiado
# tiempo y me estaba muriendo con fiebre.
class Union:

  # initializes the class computing the metrics for each case
  def __init__(self, name, types):
    self.name = name
    self.types = types
    self.unpackaged = self._calculate_space_unpackaged()
    self.packaged = self._calculate_space_packaged()
    self.optimal = self._calculate_space_optimal()

  # auxiliar method to compute the greatest common divisor
  def _gcd(self, a, b):
    if a == 0 :
      return b 
     
    return self._gcd(b % a, a)

  # auxiliar method to computhe the lowest common multiple
  def _lcm(self, a, b):
    return int(a * b / self._gcd(a, b))

  # computes the space with the structure described by the user.
  def _calculate_space_unpackaged(self):
    repre = 0
    aligns = None

    # iterate over each type to get the maximun size needed and the alignment
    for typ in self.types:
      
      if isinstance(typ, Atom):
        size = typ.repre
        typ_align = typ.align
      else:
        size = typ.unpackaged[0]
        typ_align = typ.unpackaged[1]

      # checks for the biggest possible space needed
      repre = max(repre, size)
      
      if not aligns:
        aligns = typ_align
      
      # the alignment will be the lcm of the alignment of the childs
      aligns = self._lcm(aligns, typ_align)

    # once the size is computed, calculates the unused space.
    # this neeeds to be done in a different iteration because the space left 
    # by smaller types also counts
    unused = None

    for typ in self.types:
      
      # get the information differently from Atoms than from Complex types
      if isinstance(typ, Atom):
        typ_unused = repre - typ.repre
      else:
        typ_repre = typ.unpackaged[0]
        typ_unused = (repre - typ_repre) + typ.unpackaged[2]

      # get the minimun to check if another structure uses more space
      if unused:
        print(f'saco el minimo entre {unused} y {typ_unused}')
        unused = min(unused, typ_unused)
        print('res: ', unused)
      else:
        unused = typ_unused
        print('Asigno nuevo desperdicion', unused)

    return (repre, aligns, unused)

  # does exaclty the same as the previous method but taking "packaged" attribute
  def _calculate_space_packaged(self):

    repre = 0
    aligns = None

    for typ in self.types:
      
      if isinstance(typ, Atom):
        size = typ.repre
        typ_align = typ.align
      else:
        size = typ.packaged[0]
        typ_align = typ.packaged[1]

      repre = max(repre, size)
      
      if not aligns:
        aligns = typ_align
      
      aligns = self._lcm(aligns, typ_align)

    unused = None

    for typ in self.types:

      if isinstance(typ, Atom):
        typ_unused = repre - typ.repre
      else:
        typ_repre = typ.packaged[0]
        typ_unused = (repre - typ_repre) + typ.packaged[2]

      if unused:
        unused = min(unused, typ_unused)
      else:
        unused = typ_unused

    return (repre, aligns, unused)

  # does exaclty the same as the previous method but taking "optimal" attribute
  def _calculate_space_optimal(self):

    repre = 0
    aligns = None

    for typ in self.types:
      
      if isinstance(typ, Atom):
        size = typ.repre
        typ_align = typ.align
      else:
        size = typ.optimal[0]
        typ_align = typ.optimal[1]

      repre = max(repre, size)
      
      if not aligns:
        aligns = typ_align
      
      aligns = self._lcm(aligns, typ_align)

    unused = None

    for typ in self.types:

      if isinstance(typ, Atom):
        typ_unused = repre - typ.repre
      else:
        typ_repre = typ.optimal[0]
        typ_unused = (repre - typ_repre) + typ.optimal[2]

      if unused:
        unused = min(unused, typ_unused)
      else:
        unused = typ_unused

    return (repre, aligns, unused)
    
  def __str__(self):
    return f'Soy un {self.typ}'

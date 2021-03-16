import itertools
from Atom import Atom

class Struct:

  # computes the space when the instance is initialized
  def __init__(self, name, types):
    self.name = name
    self.types = types
    self.unpackaged = self._calculate_space_unpackaged()
    self.packaged = self._calculate_space_packaged()
    self.optimal = self._calculate_space_optimal()

  # computes the metrics when the stucture of the type is exactly the same
  # as the given by the user 
  def _calculate_space_unpackaged(self):
    align = 0
    unused = 0
    
    # asign space for each type contained in the struct
    # align: represent the last used space
    # unused: count the number of spaces that have been left empty
    for typ in self.types:

      if isinstance(typ, Atom):
        typ_align = typ.align
        typ_repre = typ.repre
      else:
        typ_align = typ.unpackaged[1]
        typ_repre = typ.unpackaged[0]
      
      if align % typ_align != 0:      
        desp = typ_align - (align % typ_align)
        unused += desp
        align += desp

      align += typ_repre

    # the alignment is given by the first element described.
    first = self.types[0]
    if isinstance(first, Atom):
      al = first.align
    else:
      al = first.packaged[1]
        
    return (align, al, unused)

  # computes the metrics without taking into consideration the alignment
  # the final used space will be the space used by each inner subtype.
  def _calculate_space_packaged(self):

    used = 0
    for typ in self.types:

      if isinstance(typ, Atom):
        typ_repre = typ.repre
      else:
        typ_repre = typ.packaged[0]

      used += typ_repre

    # the alignment is given by the first element
    first = self.types[0]
    if isinstance(first, Atom):
      al = first.align
    else:
      al = first.packaged[1]

    return (used, al, 0)

  # checks which of the interations leave less spaces unused taking into
  # consideration the alignment. (bruteforce, as the prolblem is np-complete)
  def _calculate_space_optimal(self):

    # get all permutations
    original = self.types
    permutations = list(itertools.permutations(self.types))
    
    optimal_perm = None

    for permuatation in permutations:
      self.types = list(permuatation)

      space = self._calculate_space_unpackaged()

      # checks if the new permutation is better
      if optimal_perm:
        if optimal_perm[2] > space[2]:
          optimal_perm = space
      else:
        optimal_perm = space

    self.types = original
    return optimal_perm

    
  def __str__(self):
    return f'Soy un {self.typ}'

class Atom:

  # stores the information needed for the atom
  def __init__(self, name, repre, align):
    self.name = name
    self.repre = repre
    self.align = align

  def __str__(self):
    return f'Soy el atomo {self.name}'
    
import sys
from Atom import Atom
from Struct import Struct
from Union import Union

def create_variable_type(instruc, kind, type_names):
  """
  Starts the creation of a Variable type.
  """

  name = instruc[1]
  variable_type_types = []

  # check if every type has been defined previously.
  for typ in instruc[2:]:
    if not typ in type_names:
      print('No se encuentra definido el tipo: ', typ)
      return
    
    variable_type_types.append(type_names[typ])

  type_names[name] = kind(name, variable_type_types)
  print(f'Se ha creado el tipo: {name}')


def create_atomic_type(instruc, type_names):
  """
  Starts the creation of a new atomico type
  """

  if len(instruc) < 4:
    print('Por favor, utilice la cantidad de parámteros correcta.')
  else: 
    try:
      # check if the command is well structured
      name = instruc[1]
      repre = int(instruc[2])
      align = int(instruc[3])

      # creates the instance of the type
      newAtom = Atom(name, repre, align)
      if name in type_names:
        print('Ya existe un tipo de datos con ese nombre.')
      else:
        type_names[name] = newAtom
        print(f'Se ha creado el tipo atómico: {name}')
    except Exception as e:
      print('Por favor, indique una representación y alineación correctas.', e)


def get_type_info(type_obj):
  """
  Prints the information to describe the type.
  This information was already computed when the type was created.
  """
  print(f'\nLa representación del tipo de datos {type_obj.name}')

  if isinstance(type_obj, Atom):
    print(f'ocupa {type_obj.repre} bytes y debe estar alineado a {type_obj.align} bytes.')
  else:

    print('\n## SIN EMPAQUETAR ##')
    print(f'ocupa {type_obj.unpackaged[0]} bytes, debe estar alineado a {type_obj.unpackaged[1]}')
    print(f'bytes y desperdicia {type_obj.unpackaged[2]} bytes')

    print('\n## EMPAQUETANDO ##')
    print(f'ocupa {type_obj.packaged[0]} bytes, debe estar alineado a {type_obj.packaged[1]}')
    print(f'bytes y desperdicia {type_obj.packaged[2]} bytes')

    print('\n## ÓPTIMA ##')
    print(f'ocupa {type_obj.optimal[0]} bytes, debe estar alineado a {type_obj.optimal[1]}')
    print(f'bytes y desperdicia {type_obj.optimal[2]} bytes')

def main():
  """
  Executes the main menu to input the options
  """

  # dictionary to avoid names repetition
  type_names = {}

  print('Bienvenido al manejado de tipos de datos!')
  while True:
    instruc = input('\nIndique la próxima instrucción: ')
    instruc = instruc.split(' ')

    if instruc[0] == 'ATOMICO':
      create_atomic_type(instruc, type_names)

    elif instruc[0] == 'STRUCT':    
      create_variable_type(instruc, Struct, type_names)
      
    elif instruc[0] == 'UNION':
      create_variable_type(instruc, Union, type_names)

    elif instruc[0] == 'DESCRIBIR':

      # check if the type exists
      name = instruc[1]
      if name in type_names:
        
        get_type_info(type_names[name])

      else:
        print('El nombre no se encuentra definido.')

    elif instruc[0] == 'SALIR':
      sys.exit(0)
    else:
      print('Por favor, utilice una opción válida.')

main()

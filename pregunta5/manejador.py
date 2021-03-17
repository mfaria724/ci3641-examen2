import sys

def amplify_expr_spaces(expr):

  splittable_cmd = expr.replace('(', ' ( ')
  splittable_cmd = splittable_cmd.replace(')', ' ) ')

  tokens = splittable_cmd.split(' ')

  tokens = splittable_cmd.split(' ')
  while ('' in tokens): 
    tokens.remove('') 

  return tokens
  
def get_expr_type(expr, types):

  plain_cmd = ' '.join(expr)
  tokens = amplify_expr_spaces(plain_cmd)

  i = 0
  result = types[tokens[i]]
  j = 0

  while i < len(tokens) - 1:
    i += 1

    token = tokens[i]

    if not token in types:
      print(f'ERROR, el nombre "{token}" no ha sido definido.')
      return

    # check if is a constant type
    if result[j][0].isupper():
      # check that the type is exactly the same
      # if it is, can be removed from the remaining tree
      if types[token] == result[j]: 
        del result[j+1]
        del result[j]
      else:
        print(f'ERROR, No se pudo unificar {result[j]} con {types[token]}')
        return

    else:
      # set variable type for the remaining instances
      replace_token = result[j]

      for k in range(len(result)):
        if result[k] == replace_token:
          result[k] = types[tokens[i]]

      # remove type that has been satisfied
      del result[j+1]
      del result[j]

  print('Result: ', ' '.join(result))

def define_type(cmd_tokens, types):

  plain_cmd = ' '.join(cmd_tokens)
  tokens = amplify_expr_spaces(plain_cmd)

  type_name = cmd_tokens[0]

  if len(cmd_tokens[1:]) == 1:
    types[type_name] = cmd_tokens[1]
    created_type = cmd_tokens[1]
  else:
    types[type_name] = cmd_tokens[1:]
    created_type = ' '.join(cmd_tokens[1:])

  print(f'Se definió "{type_name}" con el tipo {created_type}')
  print('Types: ', types)


def main():
  print('\nBienvenido al manejador de tipos de datos polimórficos!')

  types = {}

  while True:
    cmd = input('$> ')

    tokens = cmd.split(' ')

    if tokens[0] == 'DEF':
      define_type(tokens[1:], types)
    elif tokens[0] == 'TIPO':
      get_expr_type(tokens[1:], types)
    elif tokens[0] == 'SALIR':
      sys.exit(0)
    else:
      print('Por favor, utilice un comando válido.')

main()

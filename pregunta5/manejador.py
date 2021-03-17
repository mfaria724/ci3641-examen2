import sys

def flatten_with_precedence(arr, parenthise=False):
  """
  Creates a string representation for the types created as arrays.
  """

  # if the type is already a str, leave it as it is.
  if isinstance(arr, str):
    return arr

  result = []
  for x in range(len(arr)):
    elem = arr[x]

    # if the element is a str, no need to do more
    if isinstance(elem, str):
      result.append(elem)
    else:
    # if it isn't, you need to flatten the type taking into consideration the
    # parenthisation.
      if x == len(arr) - 1:
        result.append(flatten_with_precedence(elem, False))
      else:
        result.append(flatten_with_precedence(elem, True))

  # add parenthesis when asked for
  if parenthise:
    return f"({' '.join(result)})"
  else:
    return ' '.join(result)


def amplify_expr_spaces(expr):
  """
  Cleans a little bit the input string from the user.
  This version of the interpreter is really basic, so several wrong 
  inputs can break the program execution.
  """

  # add spaces after and before the parenthesis
  splittable_cmd = expr.replace('(', ' ( ')
  splittable_cmd = splittable_cmd.replace(')', ' ) ')
  tokens = splittable_cmd.split(' ')

  # remove white spaces produces by multiple spaces 
  while ('' in tokens): 
    tokens.remove('') 

  return tokens
  
def get_expr_type(expr, types):
  """
  Evaluates recursively the type of an expression.
  """

  # parse the input expr to get the tokens
  plain_cmd = ' '.join(expr)
  tokens = amplify_expr_spaces(plain_cmd)

  i = 0
  # first token needs always to be defined, if it isn't the expr isn't valid
  token = tokens[i]
  if not token in types:
    print(f'ERROR, el nombre "{token}" no ha sido definido.')
    return
  result = types[token] if isinstance(types[token], str) else types[token].copy()

  # iterate over the tokens to check the type of every sub-expr
  while i < len(tokens) - 1:
    i += 1

    token = tokens[i]

    # catch sub-expr and get its type
    if token == '(':
      k = i + 1
      count = 0

      # check if there's a sub-expr inside the current sub-expr
      while k < len(tokens):
        if tokens[k] == '(':
          count += 1

        if tokens[k] == ')':
          if count == 0:
            final = k
          else:
            count -= 1
        k += 1

      # compute type for subexpr tokens (i+1, final-1)
      subexpr_type = get_expr_type(tokens[i+1:final], types)
      if not subexpr_type:
        return None
      token_type = subexpr_type

      # replace the chunk of the tokens that were contained in the sub-expr.
      # a token is left to emulate the space of the sub expr.
      # example
      # after: ['t1', '(', 't2', 't3', ')', 't4']
      # before: ['t1', '(', 't4']
      # even though '(' alone doesn't make sense, it fills the space of the sub-expr.
      tokens = tokens[:i] + tokens[final:]
    else:
      # check if the token is not defined 
      if not token in types:
        print(f'ERROR, el nombre "{token}" no ha sido definido.')
        return

      # if the type is an array, make a deep copy
      token_type = types[token] if isinstance(types[token], str) else types[token].copy()

    # if the result is a str because the type was so, do the computations quicker.
    if isinstance(result, str):
      # constant type
      if result[0].isupper():
        # constant type is correct
        if result == token_type:
          return token_type
        else:
          str_token_type = flatten_with_precedence(token_type)
          print(f'ERROR, No se pudo unificar {result} con {str_token_type}')
          return
      else:
      # variable type
        return token_type 
    j = 0

    # check if is a constant type
    if result[j][0].isupper():
      # check that the type is exactly the same
      # if it is, can be removed from the remaining tree
      if token_type == result[j]: 
        # IMPORTANT: this is the notion of a binary tree, a better implementation
        # will be parsing the input as a tree and evaluating.
        del result[j+1]
        del result[j]
      else:
        str_token_type = flatten_with_precedence(token_type)
        print(f'ERROR, No se pudo unificar {result[j]} con {str_token_type}')
        return

    else:
      # set variable type for the remaining instances
      replace_token = result[j]

      for k in range(len(result)):
        if result[k] == replace_token:
          result[k] = token_type

      # remove type that has been satisfied
      del result[j+1]
      del result[j]

  result = flatten_with_precedence(result)
  return result

def define_name(cmd_tokens, types):
  """
  Define a name and its type.
  """

  # little parsing of the input str
  plain_cmd = ' '.join(cmd_tokens)
  tokens = amplify_expr_spaces(plain_cmd)

  type_name = cmd_tokens[0]

  # check if it is single or multi token
  if len(cmd_tokens[1:]) == 1:
    types[type_name] = cmd_tokens[1]
    created_type = cmd_tokens[1]
  else:
    types[type_name] = cmd_tokens[1:]
    created_type = ' '.join(cmd_tokens[1:])

  print(f'Se definió "{type_name}" con el tipo {created_type}')


def main():
  """
  Executes the main client with the infinite loop.
  """

  print('\nBienvenido al manejador de tipos de datos polimórficos!')

  types = {}

  # infinite loop
  while True:
    cmd = input('$> ')

    tokens = cmd.split(' ')

    # option define by the first token
    if tokens[0] == 'DEF':
      define_name(tokens[1:], types)
    elif tokens[0] == 'TIPO':
      typ = get_expr_type(tokens[1:], types)
      if typ:
        print(typ)
    elif tokens[0] == 'SALIR':
      sys.exit(0)
    else:
      print('Por favor, utilice un comando válido.')

main()

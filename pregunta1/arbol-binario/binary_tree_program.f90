program binary_tree_program
  implicit none
  
  type binary_tree
    integer :: value
    type(binary_tree), pointer :: left => null()
    type(binary_tree), pointer :: right => null()
  end type binary_tree

  ! simple implementation of a 2-level tree, it works for multiple levels
  ! but the tree needs to be defined
  type(binary_tree) :: root
  type(binary_tree), target :: node1
  type(binary_tree), target :: node2

  node1%value = 1
  node2%value = 3
  root%value = 2
  root%left => node1
  root%right => node2

  print *, "Es de busqueda: ", esDeBusqueda(root)

contains
  ! recursive function that iterates over the nodes of the tree to check if
  ! it is a searchable tree
  recursive logical function esDeBusqueda(raiz) result(res)
    type(binary_tree) :: raiz
    logical :: is_searchable
    integer :: left_value, right_value

    !check that left side is searchable
    if (associated(raiz%left) .eqv. .true.) then
      is_searchable = esDeBusqueda(raiz%left)  
      if (is_searchable .eqv. .false.) then
        res = .false.
        return
      end if
      left_value = raiz%left%value
    else
      left_value = -huge(0)
    end if

    !check that right side is searchable
    if (associated(raiz%right) .eqv. .true.) then
      is_searchable = esDeBusqueda(raiz%right)  
      if (is_searchable .eqv. .false.) then
        res = .false.
        return
      end if
      right_value = raiz%right%value
    else
      right_value = huge(0)
    end if

    ! !the if vale is in the middle, is searchable
    if (left_value <= raiz%value .and. raiz%value <= right_value) then
      res = .true.
    else
      res = .false.
    end if

  end function esDeBusqueda

end program binary_tree_program



program church_implemenation
  implicit none
  
  print *, churchZero()
  print *, churchSucc(500)

contains
  function churchZero() result(res)
    integer :: res

    res = 0
  end function churchZero

  recursive function churchSucc(n) result(res)
    integer :: res, n

    if (n == 0) then
      res = churchZero()
    else
      res = 1 + churchSucc(n - 1)
    end if

  end function churchSucc

  function chruchAdd(n, m) result(res)
    integer :: n, m, res

    do 10 i = 1, m
      
    10 continue

  end function chruchAdd

end program church_implemenation


subroutine sum_of_square(x, y, n)
      implicit none
      integer, intent(in) :: n
      integer :: i
      real(kind=8), intent(in) :: x(n)  
      real(kind=8), intent(out) :: y  
      y = 0
      do i=1, n  
            y = y + x(i)**2
      end do  
end
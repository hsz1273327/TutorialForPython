
cdef extern from "math.h":
    cpdef double sin(double x)
    
cpdef int myfunction(int x, int y=*)

cpdef double echo_sin(double x)

cdef double _helper(double a)

cdef class A:
    cdef public int a,b
    cpdef foo(self, double x)
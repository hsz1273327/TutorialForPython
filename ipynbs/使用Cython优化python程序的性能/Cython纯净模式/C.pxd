#cython: language_level=3
cdef extern from "math.h":
    cpdef double sin(double x)
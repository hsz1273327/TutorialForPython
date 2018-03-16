#cython: language_level=3
# distutils: language = c++
# distutils: sources = vector2d.cpp


cdef extern from "vector2d.h" namespace "algebra":
    cdef cppclass Vec2d:
        Vec2d() except +
        Vec2d(double, double) except +
        double x, y
        Vec2d operator+(Vec2d)
        Vec2d operator*(float)

cdef class PyVec2d:
    cdef Vec2d c_vec2d      # hold a C++ instance which we're wrapping
    def __cinit__(self, float x, float y):
        self.c_vec2d = Vec2d(x, y)
    @property
    def x(self):
        return self.c_vec2d.x
    @property
    def y(self):
        return self.c_vec2d.y
    
    cpdef add(self,PyVec2d other):
        cdef Vec2d c
        c = self.c_vec2d+other.c_vec2d
        return PyVec2d(c.x,c.y)
    
    cpdef mul(self,float k):
        cdef Vec2d c
        c = self.c_vec2d*k
        return PyVec2d(c.x,c.y)
    
    def __add__(self,PyVec2d other):
        return self.add(other)
    
    def __mul__(self,float k):
        return self.mul(k)
    
#cython: language_level=3
import cython

if cython.compiled:
    print("Yep, I'm compiled.")
else:
    print("Just a lowly interpreted script.")
    
@cython.boundscheck(False)
@cython.ccall
def myfunction(x:cython.int, y:cython.int=2)->cython.int:
    a:cython.int
    a = x-y
    return a + x * y

@cython.cfunc
def _helper(a:cython.double)->cython.double:
    return a + 1

@cython.cclass
class A:
    a:cython.int
    b:cython.int
    def __init__(self, b=0):
        self.a = 3
        self.b = b
        
    @cython.ccall
    def foo(self, x:cython.double)->cython.double:
        print(x + _helper(1.0))
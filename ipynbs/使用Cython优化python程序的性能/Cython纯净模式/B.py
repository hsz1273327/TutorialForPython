#cython: language_level=3
import cython

if cython.compiled:
    print("Yep, I'm compiled.")
else:
    print("Just a lowly interpreted script.")
    
@cython.boundscheck(False)
@cython.ccall
@cython.returns(cython.int)
@cython.locals(x=cython.int, y=cython.int,a = cython.int)
def myfunction(x, y=2):
    a = x-y
    return a + x * y

@cython.cfunc
@cython.returns(cython.double)
@cython.locals(a = cython.double)
def _helper(a):
    return a + 1

@cython.cclass
class A:
    cython.declare(a=cython.int, b=cython.int)
    def __init__(self, b=0):
        self.a = 3
        self.b = b
    @cython.ccall
    @cython.locals(x=cython.double)
    def foo(self, x):
        print(x + _helper(1.0))
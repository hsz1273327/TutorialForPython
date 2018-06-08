#cython: language_level=3
import cython
from math import exp
if cython.compiled:
    print("Yep, I'm compiled.")
else:
    print("Just a lowly interpreted script.")
    
@cython.boundscheck(False)
@cython.ccall
@cython.returns(cython.double)
@cython.locals(x=cython.double)
def logistic(x):
    return 1/(1+exp(-x))
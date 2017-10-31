import cython

if cython.compiled:
    print("Yep, I'm compiled.")
    
else:
    print("Just a lowly interpreted script.")
    from math import sin


def myfunction(x, y=2):
    a = x-y
    return a + x * y

def echo_sin(x):
    return sin(x)
    
def _helper(a):
    return a + 1

class A:
    def __init__(self, b=0):
        self.a = 3
        self.b = b

    def foo(self, x):
        print(x + _helper(1.0))
        
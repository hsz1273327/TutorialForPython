
from distutils.core import setup
from Cython.Build import cythonize
 
setup(
    name = "vec2dapp",
    ext_modules = cythonize('vec2d.pyx')
)
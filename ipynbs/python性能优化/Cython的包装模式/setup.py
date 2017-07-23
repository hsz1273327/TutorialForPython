
from distutils.core import setup
from Cython.Build import cythonize
 
setup(
    name = "rectangleapp",
    ext_modules = cythonize('*.pyx')
)
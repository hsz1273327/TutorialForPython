
from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy

extension = Extension(
           "convolve4",
           sources=["convolve4.pyx"],
           include_dirs=[numpy.get_include()], # 如果用到numpy
           language="c++"
)

setup(
        cmdclass = {'build_ext': build_ext},
        ext_modules = cythonize(extension),
)
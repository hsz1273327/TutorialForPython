
from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import numpy
ext_modules = [
    Extension(
        "testomp",
        ["testomp.pyx"],
        #extra_compile_args=['-fopenmp'],
        #extra_link_args=['-fopenmp'],
        include_dirs=[numpy.get_include()],
        extra_compile_args=['/openmp'],
        extra_link_args=['-/openmp'],
        
    )
]

setup(
    name='hello-parallel-world',
    ext_modules=cythonize(ext_modules),
)
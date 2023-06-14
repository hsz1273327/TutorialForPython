
from distutils.core import setup
from Cython.Build import cythonize
from Cython.Distutils import build_ext
setup(
    cmdclass = {'build_ext': build_ext},
    ext_modules = cythonize("A.py",language="c++")
)
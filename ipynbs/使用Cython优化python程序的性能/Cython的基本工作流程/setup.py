from pathlib import Path
from distutils.core import setup
from Cython.Build import cythonize

dir_path = Path(__file__).absolute().parent


setup(
    ext_modules = cythonize(str(dir_path.joinpath("helloworld.pyx")))
)
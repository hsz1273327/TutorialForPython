
from setuptools import setup,find_packages
import os
pathroot = os.path.split(os.path.realpath(__file__))[0]
setup(
    name='sqrt_std',
    version='0.1.0',
    packages = find_packages(),
    entry_points = {
        'console_scripts': ['sqrt_std=lib.sqrt_std:main'],
    }
)
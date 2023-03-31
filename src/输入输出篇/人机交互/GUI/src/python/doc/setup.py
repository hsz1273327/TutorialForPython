
from distutils.core import setup
import os
pathroot = os.path.split(os.path.realpath(__file__))[0]
setup(
    name='sqrt_doc',
    version='0.1.0',
    
    scripts=[pathroot+'/sqrt_doc.py']
)
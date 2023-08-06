import sys
import os 
from setuptools import find_packages

for p in find_packages(where='.'):
    sys.path.append(os.path.join(os.getcwd(),p.replace('.','/')))

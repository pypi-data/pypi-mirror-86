# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['cotton2k', 'main', 'global', 'DailyClimate', 'PlantNitrogen']
install_requires = \
['Cython>=3.0a6,<4.0']

setup_kwargs = {
    'name': 'cotton2k',
    'version': '5.0.0a1',
    'description': 'Cotton Simulation Model',
    'long_description': None,
    'author': 'Tang Ziya',
    'author_email': 'tcztzy@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['ttsconvert']
setup_kwargs = {
    'name': 'ttsconvert',
    'version': '0.1',
    'description': 'TTS Package. Use ttsconvert.help() for help.',
    'long_description': None,
    'author': 'Nekit',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)

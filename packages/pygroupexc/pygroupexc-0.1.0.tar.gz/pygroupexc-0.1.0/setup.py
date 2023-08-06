# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pygroupexc']
setup_kwargs = {
    'name': 'pygroupexc',
    'version': '0.1.0',
    'description': 'Library for giving similar exceptions the same identifier',
    'long_description': None,
    'author': 'Frantisek Jahoda',
    'author_email': 'frantisek.jahoda@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

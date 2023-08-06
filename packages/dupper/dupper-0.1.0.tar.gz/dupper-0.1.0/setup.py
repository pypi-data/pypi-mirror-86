# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['dupper']
install_requires = \
['fire>=0.3.1,<0.4.0']

entry_points = \
{'console_scripts': ['dupper = src.dupper:main']}

setup_kwargs = {
    'name': 'dupper',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'nixiesquid',
    'author_email': 'audu817@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

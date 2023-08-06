# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gpix']

package_data = \
{'': ['*']}

install_requires = \
['pillow>=8.0.1,<9.0.0',
 'pytest>=6.1.2,<7.0.0',
 'pywavelets>=1.1.1,<2.0.0',
 'scikit-image>=0.17.2,<0.18.0',
 'scikit-learn>=0.23.2,<0.24.0',
 'tifffile>=2020.11.18,<2021.0.0']

entry_points = \
{'console_scripts': ['gpix = gpix.pyx:cli']}

setup_kwargs = {
    'name': 'gpix',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'guojian',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

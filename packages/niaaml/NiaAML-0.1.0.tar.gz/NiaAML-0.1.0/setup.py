# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['niaaml',
 'niaaml.classifiers',
 'niaaml.data',
 'niaaml.fitness',
 'niaaml.preprocessing',
 'niaaml.preprocessing.feature_selection',
 'niaaml.preprocessing.feature_transform']

package_data = \
{'': ['*']}

install_requires = \
['NiaPy>=2.0.0rc11,<3.0.0',
 'numpy>=1.19.1,<2.0.0',
 'scikit-learn>=0.23.2,<0.24.0',
 'sphinx-rtd-theme>=0.5.0,<0.6.0',
 'sphinx>=3.3.1,<4.0.0']

setup_kwargs = {
    'name': 'niaaml',
    'version': '0.1.0',
    'description': 'Automated machine learning framework written in Python.',
    'long_description': None,
    'author': 'Luka Pečnik',
    'author_email': 'lukapecnik96@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lukapecnik/NiaAML',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

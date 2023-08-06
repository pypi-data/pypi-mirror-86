# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scoptrial']

package_data = \
{'': ['*']}

install_requires = \
['jupyterlab>=2.2.9,<3.0.0',
 'matplotlib>=3.3.3,<4.0.0',
 'nbdev>=1.1.5,<2.0.0',
 'pandas>=1.1.4,<2.0.0',
 'plotly>=4.13.0,<5.0.0']

setup_kwargs = {
    'name': 'scoptrial',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'mikiokubo',
    'author_email': 'kubo@kaiyodai.ac.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

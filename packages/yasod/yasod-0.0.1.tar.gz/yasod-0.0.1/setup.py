# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yasod']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'numpy>=1.19.4,<2.0.0',
 'opencv-python>=4.4.0,<5.0.0',
 'pydantic>=1.7.2,<2.0.0']

setup_kwargs = {
    'name': 'yasod',
    'version': '0.0.1',
    'description': 'Yet another simple object detector',
    'long_description': None,
    'author': 'Michael Druk',
    'author_email': '2467184+michdr@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

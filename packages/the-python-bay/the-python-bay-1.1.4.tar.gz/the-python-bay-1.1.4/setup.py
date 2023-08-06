# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['the_python_bay', 'the_python_bay.tests']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.0,<3.0.0']

setup_kwargs = {
    'name': 'the-python-bay',
    'version': '1.1.4',
    'description': 'A python library for searching thepiratebay.org',
    'long_description': None,
    'author': 'philhabell',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_golden']

package_data = \
{'': ['*']}

install_requires = \
['atomicwrites>=1.4.0,<2.0.0',
 'pytest>=6.1.2,<7.0.0',
 'ruamel.yaml>=0.16.12,<0.17.0',
 'testfixtures>=6.15.0,<7.0.0']

extras_require = \
{':python_version < "3.7"': ['dataclasses>=0.7,<0.8']}

entry_points = \
{'pytest11': ['pytest-golden = pytest_golden.plugin']}

setup_kwargs = {
    'name': 'pytest-golden',
    'version': '0.1.0',
    'description': 'Plugin for pytest that offloads expected outputs to data files',
    'long_description': None,
    'author': 'Oleh Prypin',
    'author_email': 'oleh@pryp.in',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/oprypin/pytest-golden',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

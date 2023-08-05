# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gitgood']

package_data = \
{'': ['*']}

install_requires = \
['python-dotenv>=0.15.0,<0.16.0', 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['gg = gitgood.main:app']}

setup_kwargs = {
    'name': 'gitgood',
    'version': '0.1.0a0',
    'description': '',
    'long_description': '# gitgood',
    'author': 'QEDK',
    'author_email': 'qedk.en@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

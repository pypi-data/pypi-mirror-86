# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['forsyde',
 'forsyde.io',
 'forsyde.io.python',
 'forsyde.io.python.sql',
 'forsyde.io.python.types',
 'forsyde.io.python.types.moc',
 'forsyde.io.python.types.vertexes',
 'forsyde.io.python.types.vertexes.moc']

package_data = \
{'': ['*']}

install_requires = \
['networkx>=2.5,<3.0']

setup_kwargs = {
    'name': 'forsyde-io-python',
    'version': '0.1.3',
    'description': 'Python supporting libraries for ForSyDe IO',
    'long_description': None,
    'author': 'Rodolfo',
    'author_email': 'jordao@kth.se',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

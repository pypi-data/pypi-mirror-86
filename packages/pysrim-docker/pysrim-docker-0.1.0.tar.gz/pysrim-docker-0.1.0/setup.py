# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['srim', 'srim.docker']

package_data = \
{'': ['*']}

install_requires = \
['pysrim>=0.5.10,<0.6.0']

setup_kwargs = {
    'name': 'pysrim-docker',
    'version': '0.1.0',
    'description': 'Docker executor for PySRIM',
    'long_description': None,
    'author': 'Angus Hollands',
    'author_email': 'goosey15@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

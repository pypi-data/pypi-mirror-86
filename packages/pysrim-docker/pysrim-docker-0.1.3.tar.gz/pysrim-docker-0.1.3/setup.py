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
    'version': '0.1.3',
    'description': 'Docker executor for PySRIM',
    'long_description': '# pysrim-docker\n[![pypi-badge][]][pypi] \n\n[pypi-badge]: https://img.shields.io/pypi/v/pysrim-docker\n[pypi]: https://pypi.org/project/pysrim-docker\n\nDocker executor for PySRIM\n\n## Getting Started\nTo use this package, simply replace your `SR` or `TRIM` imports with those from `srim.docker`, e.g.\n```python\n\nfrom srim.docker import TRIM\n\ntrim = TRIM(...)\n```\n\nOut of the box, `pysrim-docker` uses the `costrouc/srim` Docker image, and writes the input and output files to a temporary directory. \n\n## How Does it Work?\n`pysrim-docker` overrides the `run()` method of the `SR` and `TRIM` classes with one that executes a bash script in a particular Docker image.\nThis script simply copies the inputs to the appropriate directory, runs the required binary, and returns the results.\n\n## Why?\nSince using Docker, I have seen its utility in hiding obscure build steps behind a simple container image. \nHowever, I prefer to write code that might be part of an analysis pipeline, rather than standalone Python modules, and so it is prefereable to \nhave the input file generation peformed on the host. An additional benefit of this is that the `pysrim` installation can be updated indepently of the Docker image.\n',
    'author': 'Angus Hollands',
    'author_email': 'goosey15@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/agoose77/pysrim-docker',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

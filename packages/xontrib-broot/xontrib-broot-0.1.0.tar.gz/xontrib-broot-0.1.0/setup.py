# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xontrib']

package_data = \
{'': ['*']}

install_requires = \
['xonsh>=0.9.20']

setup_kwargs = {
    'name': 'xontrib-broot',
    'version': '0.1.0',
    'description': 'broot support function for xonsh shell',
    'long_description': '# Overview\n[broot](https://github.com/Canop/broot) support function for xonsh shell\n\n\n## Installation\n\nTo install use pip:\n\n``` bash\nxpip install xontrib-broot\n# or: xpip install -U git+https://github.com/jnoortheen/xontrib-broot\n```\n\n## Usage\nIt adds `br` alias function. So commands like `cd` will work from broot.\n``` bash\n$ xontrib load broot\n$ br \n```\n\n## Credits\n\nThis package was created with [xontrib cookiecutter template](https://github.com/jnoortheen/xontrib-cookiecutter).\n',
    'author': 'Noortheen Raja NJ',
    'author_email': 'jnoortheen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jnoortheen/xontrib-broot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)

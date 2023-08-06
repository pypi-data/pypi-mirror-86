# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tiny_router']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tiny-router',
    'version': '0.0.2',
    'description': 'Tiny HTTP router',
    'long_description': '# tiny-router\n\nA tiny HTTP router.\n\n## Usage\n\nSee `examples/` directory of [repository](https://github.com/nekonoshiri/tiny-router).\n\n',
    'author': 'Shiri Nekono',
    'author_email': 'gexira.halen.toms@gmail.com',
    'maintainer': 'Shiri Nekono',
    'maintainer_email': 'gexira.halen.toms@gmail.com',
    'url': 'https://github.com/nekonoshiri/tiny-router',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyramid_resourceful']

package_data = \
{'': ['*']}

install_requires = \
['pyramid']

extras_require = \
{':python_version == "3.6"': ['dataclasses']}

setup_kwargs = {
    'name': 'pyramid-resourceful',
    'version': '1.0a1',
    'description': 'Resourceful routes & views for Pyramd',
    'long_description': '',
    'author': 'Wyatt Baldwin',
    'author_email': 'self@wyattbaldwin.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/wylee/pyramid_resourceful',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

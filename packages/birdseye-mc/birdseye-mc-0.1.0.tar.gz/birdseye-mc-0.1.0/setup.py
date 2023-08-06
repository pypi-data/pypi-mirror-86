# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['birdseye_mc',
 'birdseye_mc.dynmap',
 'birdseye_mc.dynmap.api',
 'birdseye_mc.dynmap.exceptions',
 'birdseye_mc.dynmap.models',
 'birdseye_mc.ui']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.7.2,<2.0.0', 'pygame>=2.0.0,<3.0.0', 'requests>=2.25.0,<3.0.0']

entry_points = \
{'console_scripts': ['birdseye = birdseye.__main__:main']}

setup_kwargs = {
    'name': 'birdseye-mc',
    'version': '0.1.0',
    'description': 'A tool for watching players on multiplayer Minecraft servers',
    'long_description': None,
    'author': 'Evan Pratten',
    'author_email': 'ewpratten@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

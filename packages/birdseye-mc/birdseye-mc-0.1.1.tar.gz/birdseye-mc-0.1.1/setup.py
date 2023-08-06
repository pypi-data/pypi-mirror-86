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
{'console_scripts': ['birdseye = birdseye_mc.__main__:main']}

setup_kwargs = {
    'name': 'birdseye-mc',
    'version': '0.1.1',
    'description': 'A tool for watching players on multiplayer Minecraft servers',
    'long_description': "# Bird's-Eye [![PyPI version](https://img.shields.io/pypi/v/birdseye_mc.svg)](https://pypi.python.org/pypi/birdseye_mc/) ![Poetry Build Suite](https://github.com/Ewpratten/birdseye/workflows/Poetry%20Build%20Suite/badge.svg)\n\n`birdseye_mc` is a GUI application for providing a multi-user bird's-eye view of players on Minecraft servers that have the [Dynmap](https://github.com/webbukkit/dynmap) plugin installed.\n\n## Installation\n\nTo install, ensure your system has `python3` and `python3-pip`, then run:\n\n```sh\npython3 -m pip install birdseye_mc\n```\n\n## Usage\n\nTo run `birdseye_mc`, use:\n\n```sh\npython3 -m birdseye_mc [dynmap url]\n```\n\nFull usage is as follows:\n\n```text\nusage: birdseye [-h] [-t] dynmap_url\n\nA tool for watching players on multiplayer Minecraft servers\n\npositional arguments:\n  dynmap_url  URL to a dynmap server\n\noptional arguments:\n  -h, --help  show this help message and exit\n  -t, --test  Show a testing player\n```\n\n## Screenshots\n\n![Screenshot](assets/screenshot.png)",
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

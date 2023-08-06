# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['xwacommap']
install_requires = \
['python-xrectsel>=1.3,<2.0', 'sh>=1.14.1,<2.0.0']

entry_points = \
{'console_scripts': ['xwacommap = xwacommap:main']}

setup_kwargs = {
    'name': 'xwacommap',
    'version': '0.1.0',
    'description': 'Interactive utility to map Wacom tablets to screen areas',
    'long_description': 'xwacommap - Interactively map Wacom table to screen area\n========================================================\n\nSynopsis\n--------\n\n`xwacommap` is a small utility that helps configuring a Wacom\ntablet to map to a selected area of the screen. It allows to\ndraw a rectangular region on the screen, then passes the\ngeometry to the `xsetwacom` tool. If the selected area is higher\nthan wide, the tablet is also rotated.\n\nRequirements\n------------\n\nThis tool requires the `xsetwacom` tool from the\n`xserver-xorg-input-wacom` package (on Debian systems).\n\nLicence\n-------\n\nThis tool is licenced under the Apache 2.0 licence.\n',
    'author': 'Dominik George',
    'author_email': 'nik@naturalnet.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://edugit.org/nik/xwacommap',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

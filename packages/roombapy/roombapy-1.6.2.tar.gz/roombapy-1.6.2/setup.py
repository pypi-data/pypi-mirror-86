# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['roombapy']

package_data = \
{'': ['*']}

install_requires = \
['paho-mqtt>=1.5.1,<2.0.0']

entry_points = \
{'console_scripts': ['roomba-connect = roombapy.entry_points:connect',
                     'roomba-discovery = roombapy.entry_points:discovery',
                     'roomba-password = roombapy.entry_points:password']}

setup_kwargs = {
    'name': 'roombapy',
    'version': '1.6.2',
    'description': 'Python program and library to control Wi-Fi enabled iRobot Roombas',
    'long_description': None,
    'author': 'Philipp Schmitt',
    'author_email': 'philipp@schmitt.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pschmitt/roombapy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)

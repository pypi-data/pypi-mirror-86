# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['majel',
 'majel.actions',
 'majel.actions.browser',
 'majel.actions.browser.handlers']

package_data = \
{'': ['*']}

install_requires = \
['kodi-json>=1.0.0,<2.0.0',
 'mycroft-messagebus-client>=0.8.1,<0.9.0',
 'python-mpv>=0.4.6,<0.5.0',
 'requests>=2.23.0,<3.0.0',
 'selenium>=3.141.0,<4.0.0']

entry_points = \
{'console_scripts': ['majel = majel.command:Majel.run']}

setup_kwargs = {
    'name': 'majel',
    'version': '0.1.0',
    'description': 'A front-end for Mycroft that allows you to do cool things like stream video or surf the web',
    'long_description': None,
    'author': 'Daniel Quinn',
    'author_email': 'code@danielquinn.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/danielquinn/majel',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

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
    'version': '0.1.1',
    'description': 'A front-end for Mycroft that allows you to do cool things like stream video or surf the web.',
    'long_description': '# Majel\n\nA [Mycroft](https://mycroft.ai/) extension that lets you do visual things with\nit as well.\n\n![Architecture](https://gitlab.com/danielquinn/majel/-/raw/ff49bdfb8d6da025788dfe39a0fc13182ec4d0b1/architecture.png)\n\n\n## What can it do?\n\nMajel listens to the [Mycroft message bus framework](https://mycroft-ai.gitbook.io/docs/mycroft-technologies/mycroft-core/message-bus)\nand performs various desktop jobs based on what it comes down that pipe.  The\nresult is that you get Mycroft\'s standard skills along with:\n\n\n### Youtube player\n\nSay `Hey Mycroft, youtube <query>` and it\'ll search Youtube for your `query`,\npick the first hit, and play it full screen in a loop.\n\n\n### Kodi\n\nIf you\'ve got a local Kodi installation *and* the video files you\'ve got in\nthere are also mounted locally, you can say `Hey Mycroft, play <query>` and\nit\'ll look for `query` in your Kodi library.  If it finds it, it\'ll play it\nwith `mpv` locally.  It\'s also smart enough to know which episodes you\'ve seen,\nso if you say `Hey Mycroft play Star Trek Deep Space Nine` and you\'ve already\nseen all of season 4, it\'ll start with s05e01.  It\'ll also pick up right where\nyou left off in that episode.\n\n\n### Netflix & Amazon Prime\n\nThe `play` keyword will also fall back to Netflix or Amazon Prime if you don\'t\nhave Kodi installed, or simply don\'t have the video you were asking for.  In\nthis case, it\'ll hit up the [Utelly API](https://rapidapi.com/utelly/api/utelly)\nto see which streaming service has the movie/show you asked for, and then point\nyour browser to that show and play the next episode.\n\nNote that this functionality requires two things: a Utelly API key (it\'s free\nfor limited use, and we\'ve got built-in caching so you\'ll never break the\n1000/mo limit) and a subscription to Netflix and/or Amazon Prime.\n\n\n### Browser Bookmarks\n\nIf you store your bookmarks in Firefox, you can say\n`Hey Mycroft, search my bookmarks for <query>`.  This will rank your bookmarks\nby relevance to your query and display a list of everything it found within a\nthreshold.  The list appears as a touchscreen-friendly UI so you can say *"Hey\nMycroft, search my bookmarks for chicken"* and select from your 12 favourite\nchicken recipes.\n\n\n## Configurability\n\nConfiguration of the skills is done separately for each skill via Mycroft\'s\nstandard settings UI on their site.  That\'s where, for example, you input your\nYouTube API key and Utelly API key.\n\nMajel is configured by way of your environment, so you can set that any way you\nlike.\n\n\n## What\'s Next?\n\nIt\'d be nice to have support for doing video calls: `Hey Mycroft, call the\nparents`, but that may not be easy to do since most video calling platforms\nseem to either be centred around scheduled group chat, or just plain\nLinux/browser hostile.\n\n\n## Colophon\n\nFor [Majel Barrett-Roddenberry](https://en.wikipedia.org/wiki/Majel_Barrett),\nwho was amazing.\n',
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

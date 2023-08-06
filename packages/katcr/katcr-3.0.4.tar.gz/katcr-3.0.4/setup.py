# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['katcr', 'katcr.engines']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.2,<4.0.0',
 'cleo',
 'cutie>=0.2.2,<0.3.0',
 'feedparser>=6.0.2,<7.0.0',
 'pytest-asyncio>=0.14.0,<0.15.0',
 'torrentmirror>=2.0,<3.0',
 'xdg>=5.0.1,<6.0.0']

extras_require = \
{':extra == "bot"': ['aiogram>=2.11.2,<3.0.0']}

entry_points = \
{'console_scripts': ['bot = katcr:bot', 'katcr = katcr:main']}

setup_kwargs = {
    'name': 'katcr',
    'version': '3.0.4',
    'description': 'KickassTorrents CLI and Telegram bot',
    'long_description': '.. image:: http://i.imgur.com/ofx75lO.png\n\nCLI client to torrent searches and streaming. Easily **search torrents** in\nmultiple providers such as KickAssTorrents, ThePirateBay, and any Jackett\nprovider.\n\n\n|pypi| |release| |downloads| |python_versions| |coverage| |pypi_versions| |actions|\n\n.. |pypi| image:: https://img.shields.io/pypi/l/katcr\n.. |release| image:: https://img.shields.io/librariesio/release/pypi/katcr\n.. |downloads| image:: https://img.shields.io/pypi/dm/katcr\n.. |python_versions| image:: https://img.shields.io/pypi/pyversions/katcr\n.. |pypi_versions| image:: https://img.shields.io/pypi/v/katcr\n.. |coverage| image:: https://codecov.io/gh/XayOn/katcr/branch/develop/graph/badge.svg\n    :target: https://codecov.io/gh/XayOn/katcr\n.. |actions| image:: https://github.com/XayOn/katcr/workflows/CI%20commit/badge.svg\n    :target: https://github.com/XayOn/katcr/actions\n\n\nTable of contents\n=================\n\n.. contents::\n  :local:\n  :depth: 3\n\n.. _features:\n\nFeatures\n--------\n\n- Display results in a nice utf-8 table\n- Interactive mode, choose and open torrent with a nice text user interface\n- Open torrent directly with your preferred client (via xdg-open)\n- Stream torrent with `torrentstream <https://github.com/XayOn/torrentstream>`_\n- Searches on all available engines until it gets results\n- Search torrents in:\n\n  + Eztv\n  + `Jackett <https://github.com/Jackett/Jackett>`_\n  + Katcr\n  + NyaaSi\n  + Skytorrents\n  + ThePirateBay\n\n\n.. code:: bash\n\n    poetry run katcr search --stream --engine Jackett --engine ThePirateBay "Big Buck Bunny" \n\n.. code:: bash\n\n    poetry run katcr search --stream --engine Jackett:eztv "Big Buck Bunny" \n\n.. image:: ./docs/stream.png\n\nInstallation\n------------\n\nThis is a python package available on pypi, just run\n\n.. code:: bash\n\n    pip install katcr\n\nOr, with streaming (see `Streaming <streaming_>`_)\n\nMake sure your python version is at least python3.8 and you\'re using that\nversion\'s pip.\n\nUsage\n-------\n\nExposes a `katcr search` command.\n\n\n--pages\n    (optional) Number of pages to search for in each engine (Except on Jackett)\n\n--engine\n    (optional) Engines available. See `Features <features_>`_ section. You can\n    use this option multiple times (as in --engine Eztv --engine ThePirateBay)\n\n--nointeractive\n    (optional) Do not open text user interface, just print all the results\n\n--open\n    (optional) Use xdg-open to open magnet link. For example to download it\n    with your preferred torrent download client.\n\n--stream\n    (optional) Use torrentstreaming to stream. See `Streaming <streaming_>`_ section\n\n\n::\n\n        USAGE\n          katcr search [--pages\xa0<...>]  [--engine\xa0<...>] [--nointeractive\xa0[<...>]]\n                       [--open\xa0[<...>]] [--stream\xa0[<...>]] <search>\n\n        ARGUMENTS\n          <search>               Search term\n\n        OPTIONS\n          --pages                Pages to search on search engines (default: "1")\n          --engine               Engines (multiple values allowed) \n          --nointeractive        Print results directly to stdout\n          --open                 Open selected magnet with xdg-open\n          --stream               Stream with torrentstream, plays using PLAYER envvar or xdg-open\n\n        GLOBAL OPTIONS\n          -h (--help)            Display this help message\n          -q (--quiet)           Do not output any message\n          -v (--verbose)         Increase the verbosity of messages: "-v" for normal output, "-vv" for more verbose output\n                                 and "-vvv" for debug\n          -V (--version)         Display this application version\n          --ansi                 Force ANSI output\n          --no-ansi              Disable ANSI output\n          -n (--no-interaction)  Do not ask any interactive question\n\n\n.. _streaming:\n\nStreaming\n---------\n\nStreaming requires `libtorrent <https://www.libtorrent.org/>`_ . \nWith libtorrent installed, you\'ll need to install katcr\'s streaming extras, for\nthat matter, install it with [stream], \n\n.. code:: bash\n\n    pip install katcr[stream]\n\nThen, just run it with \n\n.. code:: bash\n\n    poetry run katcr search --engine Jackett "Big Buck Bunny" --stream\n\nJackett Support\n---------------\n\nYou can easily use a `Jackett <https://github.com/Jackett/Jackett>`_ instance\nto search on all your configured provider.\n\nThis allows you to search on any jackett-supported site (that\'s about supported\n300 trackers). **Jackett** is probably the best way to use this software, as it\nhas a more active mantainance of the tracker sites.\n\nTo enable Jackett use, simply export your jackett URL and TOKEN as\nenvironmental variables\n\nYou can search on individual jackett providers by specifying the provider\nseparated by ":", as in:\n\n.. code:: bash\n\n    poetry run katcr --engine=jackett:thepiratebay "Big Buck Bunny"\n\n\nNote that you need to have the provider configured correctly in jackett.\n\n.. code:: bash\n\n   JACKETT_HOST=http://127.0.0.1:9117 JACKETT_APIKEY=<redacted> poetry run katcr --engine=jackett "Big Buck Bunny"\n\nOr, for a more permanent solution, write a config file to\n`${XDG_CONFIG_HOME}/katcr.ini` (wich is usually\n`~/.config/katcr.ini`) with the host and apikeys values:\n\n.. code:: ini\n\n    [jackett]\n    host = http://127.0.0.1\n    apikey = 12345 \n    # host = https://127.0.0.1\n    # host = https://127.0.0.1/prefix/\n    # ssl and prefix supported\n\n\nBot\n---\n\nKatcr comes with a bot command, connecting to telegram\n\n.. image:: docs/bot.png\n\nTo start a katcr bot, you need a bot token from the GodFather.\nOpen a conversation to `GodFather <https://t.me/botfather/>`_  to get more\ninformation on how to get a token.\n\nJust launch the bot with --token=your_token\n\n.. code:: bash\n\n        USAGE\n        console bot [--token\xa0[<...>]]\n\n        OPTIONS\n          --token                Bot token. Ask BotFather\n\n        GLOBAL OPTIONS\n          -h (--help)            Display this help message\n          -q (--quiet)           Do not output any message\n          -v (--verbose)         Increase the verbosity of messages: "-v" for normal output, "-vv" for more verbose output\n                                 and "-vvv" for debug\n          -V (--version)         Display this application version\n          --ansi                 Force ANSI output\n          --no-ansi              Disable ANSI output\n          -n (--no-interaction)  Do not ask any interactive question\n\n\n\n\nNotes\n------\n\nI like :star:, star this project to show your appreciation! \n\nThis project does not promote piracy. You can find a list of good public domain\nmovies that are available as torrents at `public domain torrents\n<https://www.publicdomaintorrents.info/>`_.\n\nLogo is based on robot cat by\n`Arsenty <https://thenounproject.com/arsenty/>`_\n',
    'author': 'David Francos',
    'author_email': 'opensource@davidfrancos.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

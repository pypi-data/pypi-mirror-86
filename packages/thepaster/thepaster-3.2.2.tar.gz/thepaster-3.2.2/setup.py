# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dpaster']

package_data = \
{'': ['*']}

install_requires = \
['Pygments>=2.7.2,<3.0.0',
 'click-aliases>=1.0.1,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'pyperclip>=1.8.1,<2.0.0',
 'requests>=2.25.0,<3.0.0']

setup_kwargs = {
    'name': 'thepaster',
    'version': '3.2.2',
    'description': 'Command-line client interface for https://dpaste.com/ pastebin',
    'long_description': '# dpaster\n\n[![Build Status](https://travis-ci.org/adder46/dpaster.svg?branch=master)](https://travis-ci.org/adder46/dpaster) [![Coverage Status](https://coveralls.io/repos/github/adder46/dpaster/badge.svg?branch=master)](https://coveralls.io/github/adder46/dpaster?branch=master) [![PyPI version](https://badge.fury.io/py/thepaster.svg)](https://pypi.org/project/thepaster/3.2.2/) [![PyPI](https://img.shields.io/badge/status-stable-brightgreen.svg)](https://pypi.org/project/thepaster/3.2.2/)\n\n**dpaster** is a command-line client interface for [dpaste](https://dpaste.com/).\n\n## Installing dpaster\n\n```sh\npip install thepaster\n```\n\n## Using dpaster\n\n```sh\n$ dpaster --help\nUsage: dpaster [OPTIONS] COMMAND [ARGS]...\n\n  Client interface for https://dpaste.com/ pastebin\n\nOptions:\n  --version  Show the version and exit.\n  --help     Show this message and exit.\n\nCommands:\n  config (c)  Configure available settings\n  paste (p)   Paste to dpaste.com\n```\n\n## Configuring dpaster\n\n```sh\n$ dpaster config --help\nUsage: dpaster config [OPTIONS]\n\n  Configure available settings\n\nOptions:\n  --show                          View current settings\n  --enable-autocp / --disable-autocp\n                                  Automatically copy the URL to clipboard\n  --enable-raw / --disable-raw    Always get raw URL\n  --default-syntax OPT            Choose default syntax (e.g. python, java,\n                                  bash)\n\n  --default-expires OPT           Choose default expiry time in days (e.g. 10)\n  --help                          Show this message and exit.\n```\n\n## Licensing\n\nLicensed under the [MIT License](https://opensource.org/licenses/MIT). For details, see [LICENSE](https://github.com/adder46/dpaster/blob/master/LICENSE).\n\n\n',
    'author': 'adder46',
    'author_email': 'dedmauz69@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)

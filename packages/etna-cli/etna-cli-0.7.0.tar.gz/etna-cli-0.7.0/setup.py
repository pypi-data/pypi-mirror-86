# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['etna_cli']

package_data = \
{'': ['*']}

install_requires = \
['click-default-group>=1.2.2,<2.0.0',
 'click>=7.0,<8.0',
 'etnawrapper>=2.5.0,<3.0.0',
 'keyring>=21.1.0,<22.0.0',
 'pendulum>=2.0.5,<3.0.0',
 'python-gitlab>=2.0.1,<3.0.0',
 'tabulate>=0.8.7,<0.9.0',
 'taskw>=1.2.0,<2.0.0']

entry_points = \
{'console_scripts': ['etna = etna_cli.etna:main',
                     'etna-cli = etna_cli.etna:main']}

setup_kwargs = {
    'name': 'etna-cli',
    'version': '0.7.0',
    'description': "Command line tool for my school's intranet",
    'long_description': '# etna-cli\n[![PyPI version](https://badge.fury.io/py/etna-cli.svg)](https://badge.fury.io/py/etna-cli)\n[![Build Status](https://drone.matteyeux.com/api/badges/matteyeux/etna-cli/status.svg)](http://drone.matteyeux.com:8080/matteyeux/etna-cli)\n[![Packagist](https://img.shields.io/badge/Docs-etna-blue)](https://etna-cli.matteyeux.com)\n\nPython tool for my school\n\n### Usage\n\n```\nUsage: etna.py [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  -v, --version  print version\n  -d, --docs     open docs page\n  --help         Show this message and exit.\n\nCommands:\n  config        Init, edit or delete etna config.\n  conversation  Conversations on intranet.\n  declare       Declaration.\n  event         Events.\n  gitlab        Gitlab.\n  project       Projects.\n  rank          Rank by promotion.\n  student       Student stuff.\n  task          Add quests and projects to TaskWarrior.\n  ticket        Tickets.\n```\n\n\n### Installation\n\nMake sure to have `taskwarrior` installed to task related stuff\n\n#### Github repository\n```bash\n$ git clone https://github.com/matteyeux/etna-cli\n$ cd etna-cli\n$ poetry install\n```\n\n#### PyPI\n- Installation : `pip3 install etna-cli`\n- Update : `pip3 install --upgrade etna-cli`\n\n### Setup\n\nMake sure to have `~/.local/bin` in your `$PATH` (`export PATH=$PATH:~/.local/bin`)\n\nIf you run etna-cli for the first time you may run `etna config init` to set credentials and optional Gitlab Token.\n```\n$ etna config init\nETNA username : demo_t\nPassword:\nAdd Gitlab API token ? [Y/n]: Y\nGitlab API token :\n```\n\nPassword and Gitlab token are not printed to STDOUT.\n\n\n### Credits\nPowered by [etnawrapper](https://github.com/tbobm/etnawrapper)\n',
    'author': 'matteyeux',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/matteyeux/etna',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

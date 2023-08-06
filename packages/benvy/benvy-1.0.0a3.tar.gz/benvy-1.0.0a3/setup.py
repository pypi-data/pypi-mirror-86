# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['benvy']

package_data = \
{'': ['*'],
 'benvy': ['container/*', 'databricks/*', 'git/*', 'hadoop/*', 'java/*']}

install_requires = \
['penvy==1.0.0a4']

entry_points = \
{'console_scripts': ['benvy-init = benvy.init:main']}

setup_kwargs = {
    'name': 'benvy',
    'version': '1.0.0a3',
    'description': 'Bricksflow framework development environment initializer',
    'long_description': "# Development environment initialization\n\nfor the [Bricksflow stack](https://github.com/bricksflow/bricksflow)\n\n### What it does:\n\n* Extends the [Pyfony dev environment initialization](https://github.com/pyfony/benvy)\n* Downloads Hadoop's `winutils.exe` and puts it into the project's `.venv` directory (Windows only) \n* Downloads **Java 1.8** binaries and puts them into the `~/.databricks-connect-java` dir\n* Creates the empty `~/.databricks-connect` file\n",
    'author': 'Jiri Koutny',
    'author_email': 'jiri.koutny@datasentics.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bricksflow/benvy',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

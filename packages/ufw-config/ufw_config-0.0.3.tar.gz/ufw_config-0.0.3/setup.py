# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ufw_config']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['ufw-config = ufw_config.ufw:main']}

setup_kwargs = {
    'name': 'ufw-config',
    'version': '0.0.3',
    'description': 'A tool for opening and closing ports with UFW.',
    'long_description': None,
    'author': 'NeonDevelopment',
    'author_email': 'root@neon-is.fun',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<3.10',
}


setup(**setup_kwargs)

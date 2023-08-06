# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cloud_radar']

package_data = \
{'': ['*']}

install_requires = \
['taskcat>=0.9.20,<0.10.0']

setup_kwargs = {
    'name': 'cloud-radar',
    'version': '0.1.0',
    'description': 'Run functional tests on cloudformation stacks.',
    'long_description': None,
    'author': 'Levi Blaney',
    'author_email': 'shadycuz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

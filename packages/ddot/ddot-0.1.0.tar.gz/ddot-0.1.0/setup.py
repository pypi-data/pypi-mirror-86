# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ddot']

package_data = \
{'': ['*']}

install_requires = \
['devinstaller-core>=0.5.1,<0.6.0', 'typer>=0.3.2,<0.4.0']

setup_kwargs = {
    'name': 'ddot',
    'version': '0.1.0',
    'description': 'Dotfile manager using the Devinstaller framework',
    'long_description': '# ddot\n\nA dotfile manager created using the Devinstaller framework\n',
    'author': 'Justine Kizhakkinedath',
    'author_email': 'justine@kizhak.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://justine.kizhak.com/projects/ddot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

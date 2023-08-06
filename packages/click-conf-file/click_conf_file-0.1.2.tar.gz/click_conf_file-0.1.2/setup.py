# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['click_conf_file']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'toml>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'click-conf-file',
    'version': '0.1.2',
    'description': 'Allows use of configuration files for setting options on click apps.',
    'long_description': None,
    'author': 'Tyler Gannon',
    'author_email': 'tgannon@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

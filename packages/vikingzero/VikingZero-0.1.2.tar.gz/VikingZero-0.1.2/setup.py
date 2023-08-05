# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['vikingzero', 'vikingzero.agents', 'vikingzero.environments']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML',
 'gym',
 'matplotlib',
 'numpy>=1.15.4,<2.0.0',
 'tensorboard',
 'tensorboardX>=2.1,<3.0',
 'torch>=1.6.0,<2.0.0',
 'tqdm']

setup_kwargs = {
    'name': 'vikingzero',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'David SeWell',
    'author_email': 'davidsewell3145@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)

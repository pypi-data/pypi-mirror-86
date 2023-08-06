# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cutters_common']

package_data = \
{'': ['*']}

install_requires = \
['kafka-python>=2.0.2,<3.0.0']

setup_kwargs = {
    'name': 'cutters-common',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Panu Oksiala',
    'author_email': 'panu@oksiala.fi',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

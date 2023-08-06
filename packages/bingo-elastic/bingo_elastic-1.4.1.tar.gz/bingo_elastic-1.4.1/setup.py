# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bingo_elastic', 'bingo_elastic.model']

package_data = \
{'': ['*']}

install_requires = \
['elasticsearch>=7.9.1,<8.0.0', 'epam.indigo>=1.4.1,<2.0.0']

setup_kwargs = {
    'name': 'bingo-elastic',
    'version': '1.4.1',
    'description': 'Bingo API for using with Elasticsearch',
    'long_description': None,
    'author': 'EPAM Systems Life Science Department',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

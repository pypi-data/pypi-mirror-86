# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_demo_lib']

package_data = \
{'': ['*']}

install_requires = \
['ipython>=7.19.0,<8.0.0']

setup_kwargs = {
    'name': 'poetry-demo-lib',
    'version': '0.1.0',
    'description': 'test poetry library publishing',
    'long_description': None,
    'author': 'webee.yw',
    'author_email': 'webee.yw@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

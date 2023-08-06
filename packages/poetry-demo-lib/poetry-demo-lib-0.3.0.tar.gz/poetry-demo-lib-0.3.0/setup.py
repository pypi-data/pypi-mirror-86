# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_demo_lib']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'poetry-demo-lib',
    'version': '0.3.0',
    'description': 'test poetry library publishing',
    'long_description': None,
    'author': 'webee.yw',
    'author_email': 'webee.yw@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['texttube']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'texttube',
    'version': '0.1.0',
    'description': 'Knowledge Distillation Toolbox.',
    'long_description': None,
    'author': 'Yevgnen Koh',
    'author_email': 'wherejoystarts@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

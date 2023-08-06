# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qx', 'qx.encodings', 'qx.file']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'qx',
    'version': '0.1.0',
    'description': 'A tool and file format for encoding and decoding data with an ASCII key',
    'long_description': '# quickxor\nA tool and file format for encoding and decoding data with an ASCII key\n',
    'author': 'Evan Pratten',
    'author_email': 'ewpratten@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

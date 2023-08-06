# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['segmentation_dxf']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.0.1,<9.0.0',
 'ezdxf>=0.14.2,<0.15.0',
 'matplotlib>=3.3.3,<4.0.0',
 'more-itertools>=8.6.0,<9.0.0',
 'numpy>=1.19.4,<2.0.0',
 'opencv-python>=4.4.0,<5.0.0']

setup_kwargs = {
    'name': 'segmentation-dxf',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'elisaAiwizo',
    'author_email': 'elisa@aiwizo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

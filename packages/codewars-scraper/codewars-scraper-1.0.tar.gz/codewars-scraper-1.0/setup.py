# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['codewars_scraper']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.5.3,<0.6.0',
 'pathvalidate>=2.3.0,<3.0.0',
 'selenium>=3.141.0,<4.0.0',
 'webdrivermanager>=0.9.0,<0.10.0']

entry_points = \
{'console_scripts': ['codewars-scraper = codewars_scraper.__main__:main']}

setup_kwargs = {
    'name': 'codewars-scraper',
    'version': '1.0',
    'description': 'Codewars scraper which allows you to parse and download your katas',
    'long_description': None,
    'author': 'dhvcc',
    'author_email': '1337kwiz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

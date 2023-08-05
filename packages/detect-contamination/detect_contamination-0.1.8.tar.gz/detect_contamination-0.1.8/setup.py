# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['detect_contamination']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['detect_contamination = '
                     'detect_contamination.__main__:main']}

setup_kwargs = {
    'name': 'detect-contamination',
    'version': '0.1.8',
    'description': 'A wrapper for centrifuge that can be used to detect contamination',
    'long_description': None,
    'author': 'Yasir Kusay',
    'author_email': 'yasir.kusay@student.unsw.edu.au',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

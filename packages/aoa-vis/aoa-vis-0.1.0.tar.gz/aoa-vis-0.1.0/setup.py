# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aoa_vis']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.4,<2.0.0', 'scikit-learn>=0.23.2,<0.24.0']

entry_points = \
{'console_scripts': ['aoa-vis = aoa_vis.gui:main']}

setup_kwargs = {
    'name': 'aoa-vis',
    'version': '0.1.0',
    'description': 'Angle of arrival visualisation.',
    'long_description': None,
    'author': 'Sam Dudley',
    'author_email': 'dudley.co.uk@gmail.com',
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

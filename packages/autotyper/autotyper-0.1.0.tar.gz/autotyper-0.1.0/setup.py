# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autotyper']

package_data = \
{'': ['*']}

install_requires = \
['PyAutoGUI>=0.9.52,<0.10.0']

entry_points = \
{'console_scripts': ['autotyper = autotyper:main']}

setup_kwargs = {
    'name': 'autotyper',
    'version': '0.1.0',
    'description': 'Paste the contents of a file to the cursor with a specified delay',
    'long_description': '# autotyper',
    'author': 'Junaid Rahim',
    'author_email': 'junaidrahim8d@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/junaidrahim/autotyper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

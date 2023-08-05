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
    'version': '1.0.1',
    'description': 'Paste the contents of a file to the cursor after a specified delay',
    'long_description': '# autotyper\n\nA simple command line tool to write the contents of a file to the cursor after a delay of few seconds. It uses\nthe `pyautogui` package to simulate the keystrokes to write out the file where the cursor is placed.\n\n\n## Installation\n\nMake sure you have Python3 installed on your system. \n\n```\npip install autotyper\n```\n\nYou will have the `autotyper` command available to go on your system.\n\n## Usage\n\n```\nusage: autotyper [-h] -f FILE -d DELAY\n\nWrite file content on cursor\n\noptional arguments:\n  -h, --help  show this help message and exit\n  -f FILE     input file containing the code\n  -d DELAY    Delay in sec before writing to the cursor\n```\n\n```\n$ autotyper -f bubblesort.c -d 10\nWriting file content to cursor in 10 sec...\n```\n\nIn this time, position your cursor to where you want to type out the text, when the delay ends, \nthe content of the file will be written to the cursor. Can be used in online exams\nto write the content of a file, where copy paste is not allowed in the text box.\n\n## License\n\nCopyright (c) **Junaid H. Rahim**. All rights reserved. Licensed under the MIT License\n\n[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)\n',
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

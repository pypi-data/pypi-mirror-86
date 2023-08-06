# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ardio']

package_data = \
{'': ['*']}

install_requires = \
['gTTS-token>=1.1.4,<2.0.0',
 'gTTS>=1.2.2,<2.0.0',
 'pdfminer.six>=20201018,<20201019']

entry_points = \
{'console_scripts': ['ardio = ardio.ardio:main_routine']}

setup_kwargs = {
    'name': 'ardio',
    'version': '1.1.0',
    'description': 'Journal article to audio book',
    'long_description': "# Ardio\nArdio (a python package) converts academic journal articles into mp3 files for listening at leisure. It removes figures, references and other contents that cannot be 'listened to.' The idea is to use it as a base application for machine learning to separate useful stuff from the rest.\n\n## Usage\n```\npip install ardio\nardio input.pdf output.mp3\n```\n\n## Contributor(s)\n[Bell Eapen](https://nuchange.ca)\n\n",
    'author': 'Bell Eapen',
    'author_email': 'github@gulfdoctor.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dermatologist/ardio',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

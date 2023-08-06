# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['manim_plugintemplate']

package_data = \
{'': ['*']}

install_requires = \
['manim>=0.1.0,<0.2.0']

setup_kwargs = {
    'name': 'manim-plugintemplate',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Jason G. Villanueva',
    'author_email': 'a@jsonvillanueva.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

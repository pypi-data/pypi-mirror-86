# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['keyosk']

package_data = \
{'': ['*']}

modules = \
['test_metadata']
setup_kwargs = {
    'name': 'keyosk',
    'version': '0.1.0a0',
    'description': 'Simple authentication provider for OAuth2 and OpenID-Connect systems',
    'long_description': '# keyosk\n\nSimple REST-full application to serve as a ready-to-deploy OAuth2 and\nOpenID-Connect authentication provider\n\n[![license](https://img.shields.io/pypi/l/keyosk)](https://opensource.org/licenses/MIT)\n[![pypi-version](https://img.shields.io/pypi/v/keyosk)](https://pypi.org/project/tox-poetry-installer/)\n[![python-versions](https://img.shields.io/pypi/pyversions/keyosk)](https://www.python.org)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n',
    'author': 'Ethan Paul',
    'author_email': '24588726+enpaul@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/enpaul/keyosk/',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

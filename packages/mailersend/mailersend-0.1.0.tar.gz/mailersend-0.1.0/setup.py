# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mailersend']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.0,<3.0.0']

setup_kwargs = {
    'name': 'mailersend',
    'version': '0.1.0',
    'description': 'Python SDK for MailerSend',
    'long_description': None,
    'author': 'Alex Orfanos',
    'author_email': 'alexandros@mailerlite.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mailersend/mailersend-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

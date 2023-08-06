# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['captif_db_config']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'captif-db-config',
    'version': '0.3',
    'description': '',
    'long_description': '# captif-db-config\n\nDatabase configuration.\n\n\n## Config file\n\nPlace a `.captif-db.ini` file in the home directory (`~` on linux). The config file should contain the following information:\n\n```\n[GENERAL]\nusername = \npassword = \nurl = \nport = \nconnection_string = \ndatabase = \n```\n',
    'author': 'John Bull',
    'author_email': 'john.bull@nzta.govt.nz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

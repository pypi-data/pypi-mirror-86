# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['test_postgres']

package_data = \
{'': ['*'],
 'test_postgres': ['.mypy_cache/*',
                   '.mypy_cache/3.8/*',
                   '.mypy_cache/3.8/_typeshed/*',
                   '.mypy_cache/3.8/collections/*',
                   '.mypy_cache/3.8/importlib/*',
                   '.mypy_cache/3.8/os/*',
                   '.mypy_cache/3.8/test_postgres/*']}

install_requires = \
['psycopg2-binary>=2.8.6,<3.0.0']

setup_kwargs = {
    'name': 'test-postgres',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Yevhen Shymotiuk',
    'author_email': 'yevhenshymotiuk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

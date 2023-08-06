# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datatosk',
 'datatosk.consts',
 'datatosk.sources',
 'datatosk.sources.databases',
 'datatosk.sources.databases.sql']

package_data = \
{'': ['*']}

install_requires = \
['google-cloud-bigquery[pandas,pyarrow]>=2.4.0,<3.0.0',
 'mysqlclient>=2.0.1,<3.0.0',
 'pandas>=1.0.1,<2.0.0',
 'pymongo>=3.11.0,<4.0.0',
 'sqlalchemy>=1.3.13,<2.0.0']

setup_kwargs = {
    'name': 'datatosk',
    'version': '1.1.0a3',
    'description': 'Python library for fetching data from different sources',
    'long_description': '<div style="text-align: center"> \n<img src="datatosk_logo.jpg" alt="Datatosk">\n<h1>Datatosk</h1>\n</div>\n\n> Python library for fetching data from different sources\n\n# Usage\nDatatosk reads configuration from the `environment variables`.\n\n## MySQL\n\nProvide particular enviroment variables:\n```\nMYSQL_HOST_[SOURCE_NAME]=\nMYSQL_PORT_[SOURCE_NAME]=\nMYSQL_USER_[SOURCE_NAME]=\nMYSQL_PASS_[SOURCE_NAME]=\nMYSQL__DB_[SOURCE_NAME]=\n```\n\n## GoogleBigQuery\n\nProvide particular enviroment variables:\n```\nGBQ_PROJECT_ID_[SOURCE_NAME]=\n```\n',
    'author': 'Miłosz Bednarzak',
    'author_email': 'milosz.bednarzak@bethink.pl',
    'maintainer': 'Miłosz Bednarzak',
    'maintainer_email': 'milosz.bednarzak@bethink.pl',
    'url': 'https://github.com/bethinkpl/datatosk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

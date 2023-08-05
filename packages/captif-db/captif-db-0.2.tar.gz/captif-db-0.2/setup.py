# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['captif_db',
 'captif_db.helpers',
 'captif_db.models',
 'captif_db.models.continuous',
 'captif_db.models.interval',
 'captif_db.tools',
 'captif_db.tools.loaders']

package_data = \
{'': ['*']}

install_requires = \
['captif-db-config>=0.3,<0.4',
 'eralchemy==1.2.10',
 'numpy>=1.19.1,<2.0.0',
 'pandas>=1.1.0,<2.0.0',
 'pymysql>=0.10.0,<0.11.0',
 'schema>=0.7.2,<0.8.0',
 'sqlalchemy-utils>=0.36.8,<0.37.0',
 'sqlalchemy>=1.3.20,<2.0.0',
 'toml>=0.10.1,<0.11.0']

setup_kwargs = {
    'name': 'captif-db',
    'version': '0.2',
    'description': '',
    'long_description': '\n# captif-db\n\nObject relational mapping for the CAPTIF database.\n\nThese are low-level methods.\n\n### Initialise database and generate a session object:\n\n```\nimport captif_db\ncaptif_db.DbSession.global_init()\nsession = captif_db.DbSession.factory()\n```\n\n### Import and use models:\n\n```\nfrom captif_db.models import Project\nprojects = session.query(Project).all()\n```\n',
    'author': 'John Bull',
    'author_email': 'john.bull@nzta.govt.nz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

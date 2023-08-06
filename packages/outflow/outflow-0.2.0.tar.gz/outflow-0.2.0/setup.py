# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['outflow',
 'outflow.core',
 'outflow.core.db',
 'outflow.core.db.alembic',
 'outflow.core.generic',
 'outflow.core.library',
 'outflow.core.logging',
 'outflow.core.pipeline',
 'outflow.core.pipeline.settings_management',
 'outflow.core.tasks',
 'outflow.core.test',
 'outflow.management',
 'outflow.management.commands',
 'outflow.management.models',
 'outflow.management.models.versions.default',
 'outflow.management.templates.pipeline_template',
 'outflow.ray',
 'outflow.ray.actors',
 'outflow.ray.tasks']

package_data = \
{'': ['*'],
 'outflow.management': ['templates/plugin_template/*',
                        'templates/plugin_template/plugin_namespace/*',
                        'templates/plugin_template/plugin_namespace/plugin_name/*',
                        'templates/plugin_template/plugin_namespace/plugin_name/models/*',
                        'templates/plugin_template/plugin_namespace/plugin_name/models/versions/*']}

install_requires = \
['aiohttp==3.6.2',
 'alembic==1.4.3',
 'black==20.8b1',
 'cloudpickle==1.5.0',
 'declic>=1.0.2,<2.0.0',
 'jinja2==2.11.2',
 'networkx>=2.4,<3.0',
 'psycopg2-binary==2.8.6',
 'ray>=1.0.0,<2.0.0',
 'simple-slurm==0.1.5',
 'sqlalchemy==1.3.20',
 'toml==0.10.1',
 'typeguard>=2.7.1,<3.0.0',
 'typing-extensions==3.7.4.2']

extras_require = \
{'tests': ['pytest>=5.2,<6.0', 'pytest-cov==2.10.1']}

setup_kwargs = {
    'name': 'outflow',
    'version': '0.2.0',
    'description': 'Outflow is a pipeline framework that can run parallelized and distributed workflows',
    'long_description': None,
    'author': 'Gregoire Duvauchelle',
    'author_email': 'gregoire.duvauchelle@lam.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nbmake']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'ipykernel>=5.3.4,<6.0.0',
 'jupyter-book>=0.8.3,<0.9.0',
 'jupyter-contrib-nbextensions>=0.5.1,<0.6.0',
 'nbstripout>=0.3.9,<0.4.0',
 'papermill>=2.2.2,<3.0.0',
 'pathlib>=1.0.1,<2.0.0',
 'pydantic>=1.7.2,<2.0.0',
 'requests>=2.25.0,<3.0.0',
 'virtualenv>=20.1.0,<21.0.0']

entry_points = \
{'pytest11': ['nbmake = nbmake.plugin']}

setup_kwargs = {
    'name': 'nbmake',
    'version': '0.0.1',
    'description': 'Pytest plugin for releasing notebooks',
    'long_description': '# nbmake\n\nPytest plugin for building notebooks into a tested Jupyterbook\n\n## Functionality\n\n1. Implements pytest plugin API to access the Jupyterbook execution runtime\n   1. This enables parallelisation with `pytest-xdist`\n2. Automates generation of Jupyterbook config and table of contents, or lets you provide your own\n3. Does not interfere with normal jupyter-book usage.\n\n## Usage\n\n### During Development\n\n```\npip install pytest nbmake\npytest --nbmake\n```\n\nthe output is a Jupyter book in a build directory:\n\n```\n_build/\n  html/ # contains jupyter book static site with test results\n  jupyter_execute/ # contains jupyter-book ipynbs\n```\n\nthis can be viewed locally for debugging\n\n```\nopen _build/html/index.html\n```\n\n## Example release process\n\n```\npytest --nbmake\nnetlify deploy dir=_build/html\n```\n\n## Roadmap\n\nJust some ideas:\n\n### Test Isolation\n\nImprove virtualisation of individual tests, e.g. to prevent `!pip install` commands contaminating the test environment.\n\n### Pytest Fixture Integration\n\nMake notebooks a first-class pytest citizen by providing a mechanism for enabling pytest fixtures\n',
    'author': 'alex-treebeard',
    'author_email': 'alex@treebeard.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/treebeardtech/nbmake',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)

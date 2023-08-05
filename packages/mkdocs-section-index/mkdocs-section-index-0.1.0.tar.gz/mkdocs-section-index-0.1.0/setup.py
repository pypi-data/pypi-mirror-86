# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mkdocs_section_index']

package_data = \
{'': ['*']}

install_requires = \
['mkdocs>=1.0,<2.0']

extras_require = \
{':python_version < "3.7"': ['dataclasses>=0.7,<0.8']}

entry_points = \
{'mkdocs.plugins': ['section-index = '
                    'mkdocs_section_index.plugin:SectionIndexPlugin']}

setup_kwargs = {
    'name': 'mkdocs-section-index',
    'version': '0.1.0',
    'description': 'MkDocs plugin to allow clickable sections that lead to an index page',
    'long_description': None,
    'author': 'Oleh Prypin',
    'author_email': 'oleh@pryp.in',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/oprypin/mkdocs-section-index',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

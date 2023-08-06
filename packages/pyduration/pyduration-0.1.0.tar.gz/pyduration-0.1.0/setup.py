# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyduration']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=0.12.1,<0.13.0', 'intervalpy>=0.1.0,<0.2.0']

entry_points = \
{'console_scripts': ['test = pytest:main']}

setup_kwargs = {
    'name': 'pyduration',
    'version': '0.1.0',
    'description': 'A calendar unit length utility library.',
    'long_description': "# pyduration\n\n![Tests](https://github.com/diatche/pyduration/workflows/Tests/badge.svg)\n\nA calendar unit length utility library for Python.\n\n# Installation\n\nWith [poetry](https://python-poetry.org):\n\n```bash\npoetry add pyduration\n```\n\nOr with pip:\n\n```\npip3 install pyduration\n```\n\n# Usage\n\nHave a look at the [documentation](https://diatche.github.io/pyduration/).\n\nBasic usage:\n\n```python\nfrom pyduration import Duration\n\ndays = Duration('1d')\nfor day in days.iterate(['2020-01-01', '2020-01-31']):\n    print(f'{day[0]} - {day[1]}')\n```\n\n# Development\n\n## Updating Documentation\n\nThe module [pdoc3](https://pdoc3.github.io/pdoc/) is used to automatically generate documentation. To update the documentation:\n\n1. Install `pdoc3` if needed with `pip3 install pdoc3`.\n2. Navigate to project root and install dependencies: `poetry install`.\n3. Generate documetation files with: `pdoc3 -o docs --html pyduration`.\n4. The new files will be in `docs/pyduration`. Move them to `docs/` and replace existing files.\n",
    'author': 'Pavel Diatchenko',
    'author_email': 'diatche@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/diatche/pyduration',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4',
}


setup(**setup_kwargs)

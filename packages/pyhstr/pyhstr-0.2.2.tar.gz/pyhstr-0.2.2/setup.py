# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyhstr']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyhstr',
    'version': '0.2.2',
    'description': 'History suggest box for the standard Python shell, IPython, and bpython',
    'long_description': '# pyhstr\n\nInspired by hstr, **pyhstr** is a history suggest box that lets you quickly search, navigate, and manage your Python shell history. At this point, it supports the standard Python shell, IPython, and bpython. The plan is to support ptpython as well, but some help is needed for that to happen (see [issue #7](https://github.com/adder46/pyhstr/issues/7)).\n\n## Installation\n\n\n```\npip install pyhstr\n```\n\n## Usage\n\nThe **standard** shell and **bpython**:\n\n  ```python\n  >>> from pyhstr import hh\n  >>> hh\n  ```\n\n**IPython**:\n\n  ```ipython\n  In [1]: import pyhstr\n  In [2]: %hh\n  ```\n\nMaking an alias should be more convenient though, for example:\n\n```bash\nalias py=\'python3 -ic "from pyhstr import hh"\'\n```\n\n## Screencast\n\n![screenshot](pyhstr.gif)',
    'author': 'adder46',
    'author_email': 'dedmauz69@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ming_p1']

package_data = \
{'': ['*']}

extras_require = \
{'docs': ['Sphinx>=1.8,<2.0',
          'sphinx-rtd-theme>=0.5.0,<0.6.0',
          'toml>=0.10.2,<0.11.0']}

setup_kwargs = {
    'name': 'ming-p1',
    'version': '0.1.2',
    'description': '',
    'long_description': '.. start-include\n\n=======\nming_p1\n=======\n\n.. image:: https://travis-ci.org/mingder78/ming-p1.svg?branch=master\n   :target: https://travis-ci.org/mingder78/ming-p1\n   :alt: Build status: Linux and OSX\n\n.. image:: https://ci.appveyor.com/api/projects/status/github/mingder78/ming-p1?branch=master&svg=true\n   :target: https://ci.appveyor.com/project/mingder78/ming-p1\n   :alt: Build status: Windows\n\n.. image:: https://readthedocs.org/projects/ming-p1/badge/?version=latest\n   :target: https://ming-p1.readthedocs.io/\n   :alt: Documentation status\n\n.. image:: https://img.shields.io/pypi/v/ming_p1.svg\n   :target: https://pypi.org/project/ming_p1/\n   :alt: Latest PyPI version\n\n.. image:: https://img.shields.io/pypi/pyversions/ming_p1.svg\n   :target: https://pypi.org/project/ming_p1/\n   :alt: Python versions supported\n\n.. end-include\n',
    'author': 'Ming-der Wang',
    'author_email': 'mingderwang@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mingderwang/ming-p1/',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.8-dev,<4.0',
}


setup(**setup_kwargs)

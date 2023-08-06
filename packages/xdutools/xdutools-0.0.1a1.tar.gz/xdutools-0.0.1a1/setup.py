# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xdutools', 'xdutools.apps', 'xdutools.auth']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0',
 'httpx>=0.16.1,<0.17.0',
 'pycryptodome>=3.9.9,<4.0.0']

extras_require = \
{'all': ['asyncclick>=7.1.2,<8.0.0',
         'colorama>=0.4.4,<0.5.0',
         'lxml>=4.6.1,<5.0.0'],
 'cli': ['asyncclick>=7.1.2,<8.0.0'],
 'old': ['click>=7.1.2,<8.0.0', 'lxml>=4.6.1,<5.0.0', 'requests>=2.25,<3.0']}

entry_points = \
{'console_scripts': ['xdu = xdutools.cli:main']}

setup_kwargs = {
    'name': 'xdutools',
    'version': '0.0.1a1',
    'description': '西电相关工具和 CLI',
    'long_description': None,
    'author': 'shoor',
    'author_email': 'shoorday@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/shoorday/xdutools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yarnlog']

package_data = \
{'': ['*']}

install_requires = \
['fire>=0.3.1,<0.4.0',
 'hurry.filesize>=0.9,<0.10',
 'pytest-cov>=2.10.1,<3.0.0',
 'requests>=2.25.0,<3.0.0']

entry_points = \
{'console_scripts': ['yarnlog = yarnlog.main:main']}

setup_kwargs = {
    'name': 'yarnlog',
    'version': '0.1.3',
    'description': 'Download Apache Hadoop YARN log to your local machine.',
    'long_description': '# yarnlog\n\n[![Tests Status](https://github.com/attomos/yarnlog/workflows/Tests/badge.svg?branch=main&event=push)](https://github.com/attomos/yarnlog/actions?query=workflow%3ATests+branch%3Amain+event%3Apush)\n[![codecov](https://codecov.io/gh/attomos/yarnlog/branch/main/graph/badge.svg?token=FQUPRYP17V)](https://codecov.io/gh/attomos/yarnlog)\n\nDownload Apache Hadoop YARN log to your local machine.\n\n## Usage\n\n```bash\n$ yarnlog <YARN_URL>\n```\n\n## Dev\n\n### Set up development environment\n\nI use Poetry to manage dependencies\n\n```bash\n$ poetry install\n$ source $(poetry env info --path)/bin/activate\n```\n\n### Debug yarnlog locally\n\n```bash\n$ poetry run yarnlog\n```\n\n### Run tests\n\n```bash\n$ pytest\n\n# coverage\n$ pytest --cov=yarnlog tests\n\n# coverage with html report\n$ pytest --cov=yarnlog --cov-report html:htmlcov tests\n```\n',
    'author': 'Nattaphoom Chaipreecha',
    'author_email': 'attomos@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/attomos/ylog',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

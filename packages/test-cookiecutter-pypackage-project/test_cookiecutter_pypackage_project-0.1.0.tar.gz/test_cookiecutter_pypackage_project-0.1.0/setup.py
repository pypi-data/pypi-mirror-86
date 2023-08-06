# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['test_cookiecutter_pypackage_project']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'test-cookiecutter-pypackage-project',
    'version': '0.1.0',
    'description': 'A test project for my cookiecutter-pypackage repo',
    'long_description': '# test-cookiecutter-pypackage-project\n\n\n[![PyPI version](https://badge.fury.io/py/test_cookiecutter_pypackage_project.svg)](https://badge.fury.io/py/test_cookiecutter_pypackage_project)\n![versions](https://img.shields.io/pypi/pyversions/test_cookiecutter_pypackage_project.svg)\n[![GitHub license](https://img.shields.io/github/license/mgancita/test_cookiecutter_pypackage_project.svg)](https://github.com/mgancita/test_cookiecutter_pypackage_project/blob/master/LICENSE)\n\n\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n\nA test project for my cookiecutter-pypackage repo\n\n\n- Free software: MIT\n- Documentation: https://test-cookiecutter-pypackage-project.readthedocs.io.\n\n\n## Features\n\n* TODO\n\n## Credits\n\n\nThis package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [`mgancita/cookiecutter-pypackage`](https://github.com/mgancita/cookiecutter-pypackage) project template.\n',
    'author': 'Marco Gancitano',
    'author_email': 'marco.gancitano@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mgancita/test_cookiecutter_pypackage_project',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

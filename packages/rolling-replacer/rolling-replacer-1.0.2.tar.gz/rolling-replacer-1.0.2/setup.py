# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src',
 'src.models',
 'src.models.strategy',
 'src.models.strategy.blue_green',
 'src.models.strategy.blue_green.steps',
 'src.utils']

package_data = \
{'': ['*']}

install_requires = \
['boto3', 'click>=7.1,<8.0']

entry_points = \
{'console_scripts': ['rolling-replacer = src.main:rolling_replacer']}

setup_kwargs = {
    'name': 'rolling-replacer',
    'version': '1.0.2',
    'description': 'Rolling replacer utility for deploy your AWS EC2 cluster.',
    'long_description': '# Rolling Replacer\n\n## Usage\n```bash\n$ rolling-replacer <strategy> <asg-blue> <tg-blue> <asg-green> <tg-green> <alb-name>\n```\n\n## Contributing\nTo contribute, please open a PR, make sure that the new code is properly tested and all the steps performed in the CI pipeline are completed successfully. \n\nWe follow the Conventional Commits specification.\n\n### Publish\n```bash\n$ poetry version <x.y.z>\n$ poetry publish\n```',
    'author': 'Matteo Martinelli',
    'author_email': 'matteomartinelli1992@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/emdotem/rolling-replacer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

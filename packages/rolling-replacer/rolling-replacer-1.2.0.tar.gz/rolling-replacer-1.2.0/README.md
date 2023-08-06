# Rolling Replacer
[![image](https://img.shields.io/pypi/v/rolling-replacer.svg)](https://python.org/pypi/rolling-replacer)
[![image](https://img.shields.io/pypi/l/rolling-replacer.svg)](https://python.org/pypi/rolling-replacer)
[![Python](https://img.shields.io/badge/python-3.8-informational)](https://docs.python.org/3/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Rolling replacer is an utility to deploy your AWS EC2 cluster.

## Installation
```bash
$ pip install rolling-replacer
```

## Usage
```bash
$ rolling-replacer <strategy> <asg-blue> <tg-blue> <asg-green> <tg-green> <alb-name>
```

## Contributing
To contribute, please open a PR, make sure that the new code is properly tested and all the steps performed in the CI pipeline are completed successfully. 

We follow the Conventional Commits specification.

### Publish
```bash
$ poetry version <x.y.z>
$ poetry publish
```
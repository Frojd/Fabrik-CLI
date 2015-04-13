# Frojd-Fabric-Cli
Cli tool for Frojd-Fabric

## Supports

### Implemented
- Generate stage folder
- __init__ in stage folder
- Individual stage files

### Not yet implemented
- Additional stage file config data
- A way of auto generating fabricrc / stage config depending on recipe
- Repro url
- Cli interface

## Requirements
To install Frojd-Fabric you need Python 2.7, virtualenv and pip.

**Packages:**

- Click
- Jinja2

## Installation
- `virtualenv venv`
- `pip install -r requirements/base.txt`

## Developing
- Coverage
	- `coverage run runtests.py`
	- `coverage report -m`
	- `coverage html`
	- `open htmlcov/index.html`
	- `coverage erase`
- Test
	- `python runtests.py`

## Code guide
- Pep8
- Flake in VIM
- TDD

## Contributing
Want to contribute? Awesome. Just send a pull request.

## Licence
Frojd-Fabric-Cli is released under the [MIT License](http://www.opensource.org/licenses/MIT).

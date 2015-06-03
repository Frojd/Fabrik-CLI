# Frojd-Fabric-Cli
Cli tool for Frojd-Fabric

## Requirements
To install Frojd-Fabric you need Python 2.7, virtualenv and pip.

## Installation

### With pip
- `pip install git+git://github.com/Frojd/Frojd-Fabric-CLI.git@develop`

### pip+git (for development)
- `git clone git@github.com:Frojd/Frojd-Fabric.git`
- `virtualenv venv`
- `source venv/bin/activate`
- `pip install --editable .`

## Usage:

### Initialize

`frojd_fabric --stages=local,stage,prod`

## Roadmap

### Implemented
- Generate stage folder
- __init__ in stage folder
- Individual stage files
- Cli interface
- Repro url

### Not yet implemented
- Additional stage file config data
- A way of auto generating fabricrc / stage config depending on recipe
- Bundled back into Frojd-Fabric


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
- TDD

## Contributing
Want to contribute? Awesome. Just send a pull request.

## Licence
Frojd-Fabric-Cli is released under the [MIT License](http://www.opensource.org/licenses/MIT).

# explora-hat
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)

Python module for interfacing with the Raspberry Pi Explora Hat.

## Installation

```bash
pip install -i https://test.pypi.org/simple/ explora-hat
```

```python
from explora.hat import gpio_manager
from explora.hat import ws281x
```

## Development
This project uses [Poetry](https://python-poetry.org/docs/#installation) for dependencies management and packaging.

```bash
# clone reporitory
git clone <repo>
cd explora-hat

# install dependecies
poetry install

# activate Python virtual environment
poetry shell

```

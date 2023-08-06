# Fitel.io Messaging Service Client


[![Python Version](https://img.shields.io/badge/python-3.8-blue)](https://www.python.org/)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![wemake.services](https://img.shields.io/badge/%20-wemake.services-green.svg?label=%20&logo=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC%2FxhBQAAAAFzUkdCAK7OHOkAAAAbUExURQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP%2F%2F%2F5TvxDIAAAAIdFJOUwAjRA8xXANAL%2Bv0SAAAADNJREFUGNNjYCAIOJjRBdBFWMkVQeGzcHAwksJnAPPZGOGAASzPzAEHEGVsLExQwE7YswCb7AFZSF3bbAAAAABJRU5ErkJggg%3D%3D)](https://wemake.services)

## Quickstart

Install

```console
pip install fitelio-ms-client
```

Then you can send messages:
```python
from fms.client import FMSClient

FMSClient().send_message(recipients=["<phone1>", "<phone2>"], text="Congratulation! You have sent first SMS")
```
or
```python
from fms.client import FMSClient

FMSClient().send_message(recipients=["<phone>"], text="Congratulation! You have sent first SMS", provider="twilio")
```

or Push message

```python
from fms.client import FMSClient

FMSClient().send_message(recipients=["<token1>", "<token2>"], text="Congratulation! You have sent first Push message", 
                         method="push")
```


## Prerequisites

You will need:

- `python3.8` (see `pyproject.toml` for full version)
- `MS Server instance` 


## Development

When developing locally, we use:

- [`editorconfig`](http://editorconfig.org/) plugin (**required**)
- [`pipenv`](https://github.com/pypa/pipenv) (**required**)
- `pycharm 2017+` or `vscode`


## Documentation

Full documentation is available here: [`docs/`](docs).

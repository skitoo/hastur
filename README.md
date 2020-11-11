![Hastur](https://github.com/skitoo/hastur/workflows/Hastur/badge.svg)

## Overview
Hastur is a web-based download management application for large files.

This project is originally a proof of concept of some notions of DDD (Domain Driven Design)
such as CQRS and Event Sourcing.

## Installation

To install it, you need to have the python [poetry](https://python-poetry.org/)
package manager installed first.

```bash
# clone the repository
git clone git@github.com:skitoo/hastur.git

# go into the project folder
cd hastur

# install dependencies via poetry
poetry install
```

## Run it

```bash
poetry run uvicorn hastur.port.web.app:web_app
```

## Author
[Alexis Couronne](https://github.com/skitoo)

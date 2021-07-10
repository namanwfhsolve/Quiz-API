# Quiz-API
[![Django CI](https://github.com/namanwfhsolve/Quiz-API/actions/workflows/ci.yml/badge.svg)](https://github.com/namanwfhsolve/Quiz-API/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/namanwfhsolve/Quiz-API/branch/main/graph/badge.svg?token=V476GWQM89)](https://codecov.io/gh/namanwfhsolve/Quiz-API)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Initial Setup

> NOTE: If you found any issue while following any of the steps below, Please create a new 
> [issue](https://github.com/namanwfhsolve/Quiz-API/issues/new) to let me fix it.

Prerequisite:
- [Poetry](https://python-poetry.org/docs/#installation)
- [Python ~3.7](https://www.python.org/downloads/)
- Recommended code editor [VS Code](https://code.visualstudio.com/download)
- Code formatting with [Black](https://github.com/psf/black)

Follow these steps to install the application in local environment:
1. Clone this repository and open the project in any code editor.

```bash
# cloning the repo
git clone https://github.com/namanwfhsolve/Quiz-API

# changing the dir to Quiz-API
cd Quiz-API
```
2. Install all the dependencies using Poetry and run setup.sh for some initial setup.
```bash
poetry install
sh ./setup.sh
```
3. Run the test to make sure everything works well.
```bash
cd server
poetry run python manange.py test
```
4. Make migrations and Start the application at localhost.
```bash
poetry run python manage.py migrate
poetry run python manage.py runserver
```
Now visit [http://localhost:8000/ping](http://localhost:8000/ping) in the browser.

***

## APIs




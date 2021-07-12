# Quiz-API
[![Django CI](https://github.com/namanwfhsolve/Quiz-API/actions/workflows/ci.yml/badge.svg)](https://github.com/namanwfhsolve/Quiz-API/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/namanwfhsolve/Quiz-API/branch/main/graph/badge.svg?token=V476GWQM89)](https://codecov.io/gh/namanwfhsolve/Quiz-API)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Initial Setup

> NOTE: If you found any issue while following any of the steps below, Please create a new 
> [issue](https://github.com/namanwfhsolve/Quiz-API/issues/new) to let me fix it.

Prerequisite:
- [Poetry](https://python-poetry.org/docs/#installation)
- [Python ^3.7](https://www.python.org/downloads/)
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

- Got to [redoc](https://quiz-api.namantam1.tech/redoc/) for getting all apis list and their detailed schema of body and response.
- To test the api got to [Swagger](https://quiz-api.namantam1.tech/swagger/).

### Some more Points:
1. For authentication JWT token is used which can be get from [login](https://quiz-api.namantam1.tech/redoc/#operation/login_create) API.
2. For creating the Quiz one can use [quiz_create_create](https://quiz-api.namantam1.tech/redoc/#operation/quiz_create_create) or can create it from [Django Admin](https://quiz-api.namantam1.tech/admin) also by going to Quiz tab.
> - username: `admin`
> - password: `password`
3. To get the quiz list use the params `live_since__lte` (less than equal to) & `available_till__gte` (greater than equal to) to get relevant reponse.
4. To attempt the quiz auth token is must for identification.
    - Send token in header in formt `Bearer {{your_access_token}}` with key `Authorization`.
5. For image API execpt only valid url of images hosted on any storage. One can use https://github.com/namantam1/tempfiler to upload their images temporary.





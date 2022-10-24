# home_budget
Small family budget web app.

## How To Use

Docker is required.

```bash
# Clone this repository
$ git clone https://github.com/Piokor/home_budget

# Go into the repository
$ cd home_budget

# Build docker image
$ docker-compose build

# Run docker image
$ docker-compose up
```

Application will be available on http://localhost/.

## How To Launch Tests

Backend tests are located in @/flask/home_budget/tests. Python (preferably 3.9) is required to launch them.

```bash
# Go into the flask catalog
$ cd home_budget/flask

# Install required packages
$ python -m pip install -r requirements.txt

# Run tests
$ python -m pytest
```
In real application there would me much more tests, these serve as an example.

[![Build Status](https://travis-ci.org/davis-mwangi/Store-Manager.svg?branch=develop)](https://travis-ci.org/davis-mwangi/Store-Manager)
[![Coverage Status](https://coveralls.io/repos/github/davis-mwangi/Store-Manager/badge.svg?branch=develop)](https://coveralls.io/github/davis-mwangi/Store-Manager?branch=develop)
[![Maintainability](https://api.codeclimate.com/v1/badges/b6c90ff724acbd039944/maintainability)](https://codeclimate.com/github/davis-mwangi/Store-Manager/maintainability)

# Store Manager

Store Manager is a web application that helps store owners manage sales and product inventory records. This application is meant for use in a single store.

## How to run the app

Clone the repo into your local machine and run below commands
```
cd Store-Manager
pip install -r requirements.txt
```
How to run the app on windows or unix 
```
Windows
set FLASK_APP=run.py

Unix
export FLASK_APP=run.py
```
Then run the command below to start the application.
```
flask run
```
## Run tests
Run the following command:
```
py.test --cov=app/tests/v1
```



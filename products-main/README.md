# Inventory Microservice
## Setup without docker
Create a python virtual environment in the project directory:
```shell
python3 -m venv venv
```
Activate the virtual env
```shell
source venv/bin/activate
```
Install the requirements
```shell
pip install -r requirements.txt
```
* You'll need a working PostgreSQL server to run the project

Create a .env file from the .env.example and fill it out
```shell
cp .env.example .env
```
## Running the project without docker
For running the project using django's default server on localhost:8000
```shell
python manage.py runserver
```

## Setting up the project using docker
Make sure you have docker installed
```shell
docker --version
```
Run the following command
```shell
docker-compose up -d
```
The project is now up and running on port 8000
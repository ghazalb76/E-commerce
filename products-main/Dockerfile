FROM python:3.10.10
WORKDIR /code
COPY requirements.txt /code
RUN pip install -r requirements.txt
COPY . /code
# The following command should be used if we don't want to use uwsgi
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
#CMD ["uwsgi", "--http", "0.0.0.0:8000", "--module", "inventory.wsgi"]
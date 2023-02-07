FROM python:3.8

RUN pip install django==3.2.17 gunicorn psycopg2

COPY ./ /Tasks_reminder/

WORKDIR /Tasks_reminder/

CMD gunicorn --bind=0.0.0.0:8080 Tasks_reminder.wsgi

FROM python:3.8

RUN pip install django==3.2.17 gunicorn psycopg2

COPY ./database.sql /app/
COPY ./manage.py /app/
COPY ./main /app/main
COPY ./Tasks_reminder /app/Tasks_reminder

WORKDIR /app

CMD gunicorn --bind=0.0.0.0:8080 Tasks_reminder.wsgi

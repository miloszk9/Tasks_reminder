# Tasks_reminder - Docker verision

Web app made to keep and share task list.

## Prerequirements (no need to install anything else)
* Docker
* Docker-compose

## Installation
```sh
$ docker-compose up -d --build
$ docker exec tasks_reminder_tasks_django_1 python manage.py migrate
```

## Usage
* Main website on 8080 local port

## Used frameworks / tools
* Docker
* Django
* PostreSQL
* Bootstrap

## Docker list
* Django server
* PostgreSQL database

## Database model screenshot
Database model (database_model.dbm) was created with pgModeler
![alt text](https://github.com/miloszk9/Tasks_reminder/blob/master/example%20screenshots/pgmodeler_screenshot.PNG?raw=true)

## Example usage screenshots

### Tasks list preview
![alt text](https://github.com/miloszk9/Tasks_reminder/blob/master/example%20screenshots/tasks_list.PNG?raw=true)

### Adding or editing task form
![alt text](https://github.com/miloszk9/Tasks_reminder/blob/master/example%20screenshots/tasks_create.PNG?raw=true)

### Friends list
![alt text](https://github.com/miloszk9/Tasks_reminder/blob/master/example%20screenshots/friendlist.PNG?raw=true)

### Tasks sharing
![alt text](https://github.com/miloszk9/Tasks_reminder/blob/master/example%20screenshots/task_share.PNG?raw=true)

### Birthday reminder
![alt text](https://github.com/miloszk9/Tasks_reminder/blob/master/example%20screenshots/birthday_reminder.PNG?raw=true)

### Mobile and tablet version
![alt text](https://github.com/miloszk9/Tasks_reminder/blob/master/example%20screenshots/tablet_version.PNG?raw=true)

Made by: Miłosz Kaszuba

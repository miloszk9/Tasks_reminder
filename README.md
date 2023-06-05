# Tasks_reminder - Kubernetes verision

Web app made to keep and share task list.

## Prerequirements (no need to install anything else)
* Docker
* Docker-compose

## Image build
```sh
$ docker buildx build --platform linux/amd64,linux/arm64 -t mylosz/tasks-reminder:<tag> --push .
```

## Usage
* Main website on 8080 local port

## Used frameworks / tools
* Kubernetes
* Django
* PostreSQL
* Bootstrap
* Letsencrypt

## Docker list
* Django server
* PostgreSQL database

## How it was deployed
* Self-deployed K3S cluster on Oracle Cloud
* TLS certificates from Letsencrypt (with cert-manager usage)

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

# Introduction

# Introduction

This application is a powerful document management system, designed to digitize
documents easily. As a fork of
the [paperless-ngx](https://github.com/paperless-ngx)
project, our version extends and customizes the functionality of the original
project to better suit our specific needs and be an entrance for a broader
document management system.

In this enhanced version, We have optimized the system for better performance
and scalability. This
application uses Docker for easy setup and deployment.

## Requirements:

- Docker installed on your system

- Ensure the following files are present:

  - `docker-compose_dev/docker-compose-dev.yml`
  - `docker-compose_dev/docker-compose-dev.env`


- The docker container will use postgres and redis as the database,
you don't need to install them on your system.


## How to Run the Backend:

1. Navigate to the `docker-compose_dev` directory and run:

   ```shell
   docker-compose -f docker-compose-dev.yml up
   ```

   This will create the following 4 containers:

- Postgres
- Redis
- paperless-front
- paperless-webserver

#### Create a SuperUser:

From outside the containers, run:

```shell
docker-compose -f docker-compose-dev.yml run --rm webserver createsuperuser
```

OR, from inside the `webserver` container:

1. Execute a console in the container:

   ```shell
   docker exec -it <container-name-or-id> bash
   ```

2. Create a superuser:

   ```shell
   python3 manage.py createsuperuser
   ```

#### Run the Webserver:

1. Execute a console in the `webserver` container:

   ```shell
   docker exec -it <container-name-or-id> bash
   ```

2. Run the Django app in debug mode:

   ```shell
   python3 manage.py runserver 0.0.0.0:8000
   ```

#### Create and Run the Containers:

1. Navigate to the `docker-compose_dev` directory and run:

   ```shell
   docker-compose -f docker-compose-dev.yml up
   ```

This will create the following 4 containers:

- Postgres
- Redis
- paperless-front
- paperless-webserver

#### Create a SuperUser:

From outside the containers, run:

```shell
docker-compose -f docker-compose-dev.yml run --rm webserver createsuperuser
```

OR, from inside the `webserver` container:

1. Execute a console in the container:

   ```shell
   docker exec -it <container-name-or-id> bash
   ```

2. Create a superuser:

   ```shell
   python3 manage.py createsuperuser
   ```

## Kafka messages

Kafka is used to send messages and log events in the system. The messages are
sent to the `paperless` topic. The messages are in JSON format and have the
following fields:

{`timestamp`: The time at which the message was sent, <br>
`payload`: The event that occurred, <br>
`project`: "PROJECT_NAME", <br>
  `action`: "Reception account created",<br>
  `site`: "NC",<br>
  `correlationId`: "NC", <br>
  `dossierId`: "NC",<br>
  `operatorId`: 999,<br>
  `timestamp`: 1716382987820}

Here is an example of a payload:

  `payload`: {<br>
    `registrationNumber`: "08124152",<br>
    `technicalClientId`: "100000000099999",<br>
    `company`: "EXPL",<br>
    `lastName`: "last_name",<br>
    `firstName`: "first_name",<br>
    `dateOfBirth`: "2000-01-01",<br>
    `email`: "mail@mail.com",<br>
    `phoneNumber`: "",<br>
    `employee_in_collaborator_db`: "PROJECT_NAME",<br>
  }


## How to Run the Backend:

1. Navigate to the `docker-compose_dev` directory and run:

   ```shell
   docker-compose -f docker-compose-dev.yml up
   ```

This will create the following 4 containers:

- Postgres
- Redis
- paperless-front
- paperless-webserver

#### Create a SuperUser:

From outside the containers, run:

```shell
docker-compose -f docker-compose-dev.yml run --rm webserver createsuperuser
```

OR, from inside the `webserver` container:

1. Execute a console in the container:

   ```shell
   docker exec -it <container-name-or-id> bash
   ```

2. Create a superuser:

   ```shell
   python3 manage.py createsuperuser
   ```

#### Run the Webserver:

1. Execute a console in the `webserver` container:

   ```shell
   docker exec -it <container-name-or-id> bash
   ```

2. Run the Django app in debug mode:

   ```shell
   python3 manage.py runserver

### Generate pipfile.lock :

Command : pipenv lock or pipenv install --dev

#### Prerequisite :

To install psycopg2 = "*" and mysqlclient = "==2.1.0",

we need these packages :

- sudo apt install libmysqlclient-dev
- sudo apt install libpq-dev -->

## How to update translations :

### Django backend :

Django backend uses :<br>
`{% translate %}`
and `django.utils.translation.gettext()` to manage translations. You can modify local files to update translations. Once it is done :
<br>
- From inside webserver container, run :
  ```
    # will update all .po files (change line numbers and add new translations)
    django-admin makemessages --all

    # you can then change the labels in the .po files

    # then run, it will compile the .po files to .mo files
    python3 manage.py compilemessages
  ```

### Angular frontend :

Angular frontend uses :<br>
`{{ 'TRANSLATION_KEY' | translate }}` and `i18n` service to manage translations. You can modify local files to update translations. Once it is done :
<br>
- From inside frontend container, run :
  ```
    # will update all tags (change line numbers and add new)
    npm run extract-i18n

    # you can then change the labels in the locale files
  ```

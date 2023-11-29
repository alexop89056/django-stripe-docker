# Stripe based payment UI with Django + Docker

## Overview

This project is a basic template based on Django Docker services to provide connection between stripe payment system and django.

## Technologies that have been used
![Django](https://img.shields.io/badge/django-darkgreen?style=for-the-badge&logo=django&logoColor=white&labelColor=darkgreen)
![Gunicorn](https://img.shields.io/badge/gunicorn-green?style=for-the-badge&logo=gunicorn&logoColor=white&labelColor=green)
![Nginx](https://img.shields.io/badge/nginx-darkgreen?style=for-the-badge&logo=django&logoColor=white&labelColor=darkgreen)
![PostgresSQL](https://img.shields.io/badge/postgresql-blue?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/docker-5b5bfe?style=for-the-badge&logo=postgresql&logoColor=white)


## Installation

To install the project, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/alexop89056/django-stripe-docker.git
2. Navigate to the project directory:
 
    ```bash
    cd django-stripe-docker

3. Run building of docker-compose

    ```bash
    docker-compose up --build

## Project Structure
- ``/backend``: This folder consists of Django backend application.
- ``/nginx``: This folder consists of nginx basic config.
- ``/docker-compose.yml``: This file contains main logic of starting docker containers (services).

## After Starting
- For the first step after you start the docker-compose you need to open bash terminal in the running container:

   ```bash
   docker exec -it backend_app /bin/bash
  
- Then you need to migrate all database data (be sure that you are in the main djangoTestStripe folder:

    ```bash
   python manage.py migrate
  
- You need to create ``settings_local.py`` file in djangoTestStripe folder and write 2 variables in it:
   ```python
   STRIPE_TOKEN='Your stripe private token'
   PUBLIC_STRIPE_TOKEN='Your stripe public token'
  
- [OPTIONAL] Create a superuser to provide access to admin panel:

    ```bash
   python manage.py createsuperuser

## Notes
- File ``settings_local.py`` : Is used to overwrite settings from ``settings.py`` , y ``settings_local.py`` file has more priority. ``settings_local.py`` should be located in djangoTestStripe folder.


## License
This project is licensed under the MIT License - see the [main page](https://mit-license.org/) for the details.

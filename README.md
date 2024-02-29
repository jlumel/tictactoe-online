# TicTacToe

## Description

TicTacToe is a web application where users can register to play Tic Tac Toe online

## Technology
The App uses Django on the backend and Javascript with jQuery on the frontend. It uses two databases. One SQL database (SQLite on development and PostgreSLQ on production). In addition to that, the application uses Redis as a second database to manage matches information and Websocket to allow communication between clients so matches online are possible.

## Databases

The main SQL database is SQLite and is created automaticly by Django when building commands are run.

The Redis database has to be created and run outside the App. On production use environment variables to configure it. By default the Redis configuration on Development environment is:

**host='localhost'**

**port=6379**

**db=0**

## Build and Start Commands

- Build on development

**pip install -r requirements.txt**

**python manage.py makemigrations tictactoe**

**python manage.py migrate**

- Start on development

**python manage.py runserver**

For production use build.sh and start.sh files. There are render and nginx configuration files. If you are not using them delete them and use your own.
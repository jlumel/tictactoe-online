# TicTacToe

## Description

TicTacToe is a web application where users can register to play Tic Tac Toe online

## Distinctiveness and Complexity

The project is sufficiently distinct from the projects in the course as it is an online game which was not the object of any of the others projects. Also the way the game works is different from the way other projects work because is base in detecting user clicking and connecting different clients with each other. The complexity requirements are also met as it uses Django and Javascript and has two models for an SQL database: one for Players that takes advantage from the AbstractUser Model from Django and another for matches. In addition to that, the application uses Redis as a second database to manage matches information and Websocket to allow communication between clients so matches online are possible. On the frontend, the application uses jQuery library for the match room logic. The reason for that is that it works a lot adding and removing classes and jQuery makes that easier. The application is also mobile-responsive.

## Files

### Project folder

All files created in this folder are created automaticly by Django but its configuration was modify to met the requirements for this project. Here are the configurations for the databases, middlewares, websocket, static files among other.

### .env.example

In this file we can see the environment variables needed for this project to run correctly. For Development environment the only ones needed are DEVELOPMENT and SECRET_KEY.

### App folder

In the tictactoe application folder there are all the files where the app is developed. We have a folder for HTML templates and six Python files for backend code.

- Templates

-- error_page.html: a template to redirect users in case of errors. It can receive variables to customize the message and the path where the go-back button points to.

-- index.html: Is the home page of the App. If the user is logged in it shows a button to start playing. Otherwise, it shows two buttons and a message to register or log in.

-- layout.html: It shows in every view and it contains the navigation bar for the App. It also renders conditionally whether the user is logged in or not. If they are logged in the can see the rankings, match history and logout buttons. If they are not logged in they can see the log in and register buttons.

-- lobby_list.html : Shows a list of lobbies created by other players. If you have a lobby created in other window you wont't be able to see it here. The list updates itself everytime someone creates or eliminates a lobby using Websocket.

-- lobby.html: When a user creates or joins a lobby is presented with this page. It shows players in the lobby and the start button that is disabled when there is only one player. If the host leaves the lobby is eliminated and if there was a second player it gets redirected to an error page that informs them that the host disconnected.

-- match_room.html: When a user in a lobby starts the game, a countdown starts and after 5 seconds both players are redirected to the match room. Here they can play as many matches of tic tac toe they want. If any player leaves the room is eliminated and the other player is redirected to an error page that informs them the opponent disconnected. Any time a new game is started the cross and circle asigment to players is inverted.

-- playing_options.html: Is a page where players decide if they want to create a lobby or join an existing one.

-- ranking.html: It shows a table with the ranking of all players registered in the App order by number of wins in descendant order. It also shows wins, losses and draws of each player.

-- match_history.html: It shows a list games played by the user displaying opponent, result and date of each match.

-- login.html: A form to log in

-- register.html: A form to register

- admin.py: The configuration for the superuser to be able to see and edit main database

- consumers.py: The consumer for the websocket server. Here is the logic for the communication between clients that allows lobby creation, lobby access and matchs to be played online. It uses a Redis database to manage lobbies and matches information and share that information between clients.

- routing.py: It defines the websocket urls. We use three urls, one for the lobby list view, one for the lobby view and other for the match room view.

- urls.py: It defines the routes for the Django App.

- views.py: The logic to render the views and manage the main database.

- models.py: Where the main database models are defined. There are to models, one for players information(Player) and the other for matches information(Match).

- static: A folder where all the static files are stored. There are some images, the favicon, the css file, the Roboto font file, jquery file and a utils.js file where the logic for win and draw checking during matches is.

## Build and Start Commands

- Build

pip install -r requirements.txt

python manage.py makemigrations tictactoe

python manage.py migrate

- Start

python manage.py runserver
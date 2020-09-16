                                                ONLINE TIC-TAC-TOE

Description:

Users connected to the internet can play the game, will be connected at random and be able to play with one another.

No more playing TIC-TAC-TOE from the same device and no user account creation needed. 


Installation:

Run the 'createGame.py' and 'createFirstRow.py' files as lambda files thereby creating 'Game' dynamoDB table with 'gameId' as the 
partition key and the first item with field 'count'.

Create the rest of the python files as lambda files and configure the RESTAPIs in API Gateway with lambda proxy and CORS enabled.

Host a S3 static website with 'static_hosting_index.html' as the index file and 'static_hosting_core.html'. The two files are used
to connect two players and run the game respectively. The front-end interacts with RESTAPIs and Ajax.


Usage:

Click on the 'Start' button to get started.

Once a opponent is found, you will be assigned either 'X' or 'O'.

If it is your turn,  within 30 sec, click on the button you wish to place your letter at. Timer will be displayed.

If it is your opponent's turn, just wait. You will be notified if it is your turn.

Whoever forms a horizontal/vertical/diagonal sequence of the assigned letter first, wins.



Game Link:

http://online-tictactoe.s3-website.us-east-2.amazonaws.com


# Alpha-Zero
Alpha zero is the game bot which plays Tic-Tac-Toe game. A goal of the bot is to beat humans in Tic-Tac-Toe. I choose Tic-Tac-Toe game because of limitation of CPU power. Alpha-zero bot applies to almost all board games like Chess, Go and count four etc. This game environment has 5 rows, 5 columns. To win this game player has to match 4 "O"s and 4 "X"s. It makes this game more difficult than normal Tic-Tac-Toe.

References:  
1. AlphaZero: Mastering Chess and Shogi by Self-Play with a General Reinforcement Learning Algorithm
2. AlphaGo Zero: Mastering the game of Go without human knowledge

## ScreenShot
UI for game
- ![GamePlay](https://raw.githubusercontent.com/fahim9898/alpha_zero/master/video/playing.gif)

## Motivation
I have inspired by two projects
- First, one is google deepmind research team's project in which they have developed Alpha zero bot which defeated the world champion of GO "Mr Lee Sedol"
- Second one is [Tanmay Backshi youtube vieo](https://www.youtube.com/watch?v=9XVmTMv2TOE), He has made game bot of 2048 game using alpha-zero algorithm. I learned many things from this video

### Requirements
To play with Trained AI models
- python==3.6.5
- Keras==2.3.1
- Keras-Applications==1.0.8
- Keras-Preprocessing==1.1.0
- tensorflow==2.0.0
- Flask==1.1.2
- Flask-SocketIO==4.3.0

## How to install
Install all dependency 
```sh
conda create -n <your_env_name> python=3.6.5
pip install -r requirements.txt
```

### Getting statted
activate env
```sh
conda activate your_env_name
```
To play with game on browser
```
python web_server_alphazero.py
```
If you want train the bot policy model
```
python train.py
```

### Moduls
>Using Socketio we communicate between web server and client to realtime data exchange
>web_server_alphazero.py : Is a web server.Provide api take game input as game state , last move and current player and provide output as action position
- game.py : Game environment 
- mcts.py : Implementation of monte carlo tree search
- policy.py : Create model and fit Model
- train.py :  All training done here

### Source
* [Basic about Alpha-Zero](https://medium.com/@jonathan_hui/alphago-zero-a-game-changer-14ef6e45eba5)
* [Tanmay Bakshi youtube video](https://www.youtube.com/watch?v=9XVmTMv2TOE)

**Tips for training:**
- Board has 5 * 5 grid and 4 rows match. Bot achive good performance in 1000-1500 game plays and take time 2 to 3 hours
# Alpha-Zero
Alpha zero is game bot for which play Tic-Tac-Toe game. A goal of the bot is beat humans in Tic-Tac-Toe game. I choise Tic-Tac-Toe game because limitation of cpu powers. Alpha-zero bot also working almost all board game like Chess , Go and count four. Game environment of Tic-Tac-Toe have 5 rows , 5 column and 4( "O" and "X" Match) therefor game make deficult then normal game.

References:  
1. AlphaZero: Mastering Chess and Shogi by Self-Play with a General Reinforcement Learning Algorithm
2. AlphaGo Zero: Mastering the game of Go without human knowledge

## ScreenShot
UI for game
![out](https://raw.githubusercontent.com/junxiaosong/AlphaZero_Gomoku/master/playout400.gif)

## Motivation
I have two Motive for making this project
    - Inspired by google deepmind research team they make alpha zero bot defied world champion of GO "Mr Lee Sedol"
    - Watch Tanmay Bakshi youtube video [link](https://www.youtube.com/watch?v=9XVmTMv2TOE) , his make game bot of 2048 game using alpha-zero algorithm . Lots of thing learn from that video

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

### getting statted
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
[Tanmay Bakshi youtube video](https://www.youtube.com/watch?v=9XVmTMv2TOE)
[Basic about Alpha-Zero](https://medium.com/@jonathan_hui/alphago-zero-a-game-changer-14ef6e45eba5)

**Tips for training:**
- Board have 5 * 5 board have 4 row. For this case,we obtain good model in around 1000-1500 self-play game
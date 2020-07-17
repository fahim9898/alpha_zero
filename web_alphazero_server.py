import policy
import mcts
import game
import sys
import numpy as np
import random
from collections import deque

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

sys.setrecursionlimit(100000)


class Training_Pipe_Line:
    def __init__(self, init_model=None):
        self.board_width = 5
        self.board_height = 5
        self.show_board = True
        self.n_in_row = 4
        self.n_playout = 400  # num of simulations for each move
        self.c_puct = 5
        self.self_play_batch_size = 1
        self.number_game_play_training = 1500
        self.buffer_size = 10000
        self.learning_rate = 2e-3
        self.epochs = 5
        self.batch_size = 128

        self._is_selfplay = 0
        self.init_model = True

        self.buffer = deque(maxlen=self.buffer_size)

        self.board = game.Board(self.board_width,
                                self.board_height,
                                self.n_in_row)
        if self.init_model:
            self.policy_value_net = policy.PolicyValueNet(self.board_width,
                                                          self.board_height, "current_policy_5_5_4_level_6.model")
        else:
            self.policy_value_net = policy.PolicyValueNet(self.board_width,
                                                          self.board_height)
        # print("llll")
        self.mcts_player = mcts.MCTS_Player(self.policy_value_net.policy_value_fn,
                                            c_put=self.c_puct,
                                            n_playout=self.n_playout,
                                            _is_selfplay=self._is_selfplay)

    def get_equi_data(self, play_data):
        # print(play_data)
        extend_data = []
        for state, prob, winner in play_data:
            for i in [1, 2, 3, 4]:

                # Rotate

                equi_state = np.array([np.rot90(s, i) for s in state])
                equi_prob = np.rot90(np.flipud(
                    prob.reshape(self.board_height, self.board_width)
                ), i)

                extend_data.append([equi_state,
                                    np.flipud(equi_prob).flatten(),
                                    winner])

                # flip horizontal

                equi_state = np.array([np.fliplr(s) for s in state])
                equi_prob = np.fliplr(equi_prob)
                extend_data.append([equi_state,
                                    np.flipud(equi_prob).flatten(),
                                    winner])

        return extend_data

    def self_play(self, is_show=False):
        self.board.reset_board()

        state, mtcs_prob, current_players = [], [], []

        while True:
            t_move, prob = self.mcts_player.get_action(self.board, 1e-3, 1)
            state.append(self.board.current_state())
            mtcs_prob.append(prob)
            current_players.append(self.board.get_current_player())
            self.board.do_move(t_move)

            end, winner = self.board.end_game(1)

            if is_show:
                self.board.graphic_display()

            if end:
                winners_z = np.zeros(len(current_players))
                if winner != -1:
                    winners_z[np.array(current_players) == winner] = 1.0
                    winners_z[np.array(current_players) != winner] = -1.0

                    self.mcts_player.reset_player()

                    # print(winners_z)
                return winner, zip(state, mtcs_prob, winners_z)

    def collect_self_play_data(self, n_time_play_game=1):
        for _ in range(n_time_play_game):
            winner, play_data = self.self_play(self.show_board)
            play_data = list(play_data)[:]
            # print(play_data)

            # Rotate and flip left-right data

            equi_data = self.get_equi_data(play_data)
            self.buffer.extend(equi_data)

            print("GAME COMPLETED AFTER {} STEPS , LENGTH OF BUFFER {}".format(
                len(play_data), len(self.buffer)))
        # print(self.buffer , len(self.buffer))

    def play_with_human(self):
        first_move = 0
        print("PLEASE CHOSE FIRST TURN BETWEEN COMPUTER AND HUMAN : 0 for Compuer , 1 for Human")
        first_move = int(input()) % 2
        count = 0
        while True:
            if count % 2 == first_move:
                t_move, prob = self.mcts_player.get_action(self.board, 1e-3, 1)
                self.board.do_move(t_move)
                self.get_equi_data([[self.board.current_state(), prob, 1]])
                # exit()
            else:
                print("Enter x , y")
                pos = input().split()
                pos_x = int(pos[0]) - 1
                pos_y = int(pos[1]) - 1
                self.board.do_move(pos_x * self.board_width + pos_y)
            self.board.graphic_display()
            end, winner = self.board.end_game(1)
            # print(end , winner)
            count += 1
            if end:
                print(
                    "----------------------------------------WINNER-------------------------------", winner)
                break
        print(self.mcts_player.mcts.root_node._children)
        print("okay")

    def policy_update(self):
        print(np.shape(self.buffer))
        mini_batch = random.sample(self.buffer, self.batch_size)
        # print(len(mini_batch))
        # print(mini_batch[0])
        # state_batch , mcts_probs_batch , winner_batch =[] , [] , []
        # for i in range(len(mini_batch)):
        #     state_batch.append(mini_batch[i][0])
        #     mcts_probs_batch.append(mini_batch[i][1])
        #     winner_batch.append(mini_batch[i][2])
        state_batch = [data[0] for data in mini_batch]
        mcts_probs_batch = [data[1] for data in mini_batch]
        winner_batch = [data[2] for data in mini_batch]

        # print(mcts_probs_batch)

        for i in range(self.epochs):
            loss, entropy = self.policy_value_net.train_step(
                state_batch,
                mcts_probs_batch,
                winner_batch,
                self.learning_rate)
            print("loss:{} after -> {} epochs".format(loss, i))

    def run(self):
        # for i in range(self.number_game_play_training):
        #     print("========================================== GAME {} ================================================".format(i))
        #     self.collect_self_play_data(self.self_play_batch_size)
        #     if(len(self.buffer) > self.batch_size):
        #         self.policy_update()

        #     if(i%10 == 0 and i != 0):
        #         self.policy_value_net.save_model('./current_policy_5_5_4.model')

        self.play_with_human()
        # self.self_play(True)

    def server_response(self, width, height, n_match,  state,  current_player, last_move):
        print("Hello")
        temp_board = game.Board(width, height, n_match,
                                False, state, current_player, last_move)
        t_move, prob = self.mcts_player.get_action(temp_board, 1e-3, 1)
        temp_board.do_move(t_move)
        temp_board.graphic_display()
        end_game = temp_board.end_game()
        return end_game , t_move


# print("okay")
tp = Training_Pipe_Line()
""" tp.server_response(5, 5, 4, [0, 0, 0, 0, 1,
                             0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0], 1, 12) """ 
# tp.run()
""" 0 , 0 , 0 , 0 , 0 ,
2 , 2 , 2 , 0 , 0 , 
1 , 1 , 1 , 1 , 0 ,
0 , 0 , 0 , 0 , 0 ,
0 , 0 , 0 , 0 , 0 , """


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')

@socketio.on("send state" , namespace = "/private")
def return_action(data):
    b_s = data["board_size"]
    board_state =data["board_state"]
    current_player_ = data["current_player"]
    last_move_ = data["last_move"]
    # print(b_s , board_state , current_player_ , last_move_)
    # print("-----------------------------------------------------REQUEST SEND------------------------------------------------")
    game_status , action= tp.server_response(b_s, b_s , 4, board_state, current_player_,last_move_)
    # tp.server_response(5, 5, 4, [0, 0, 0, 0, 1,
    #                              0, 0, 0, 0, 0,
    #                              0, 0, 0, 0, 0,
    #                              0, 0, 0, 0, 0,
    #                              0, 0, 0, 0, 0], 1, 12)
    # print(game_status , "++++++++++++++++++++++++++++++++++++++")
    
    emit('server response' , {"game_status": game_status , "action": str(action)})

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0")
    socketio.run(app)

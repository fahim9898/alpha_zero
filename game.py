import numpy as np

class Board:
    def __init__(self , width , height , n_match , init_bord = True , state = None , current_player = 0 ,last_move =-1):
        self.width = width
        self.height = height
        self.n_match = n_match
        # self.state = np.zeros(width * height)
        self.state = {}
        # self.available_state = {}
        if init_bord:
            for i in range(width * height):
                self.state[i] = 0
                self.available_state = [item for item in range(width * height)]
        else:
            for i in range(width * height):
                self.state[i] = state[i]
                # all_state = [item for in range(width * height)]
            self.available_state = [item for item in range(width * height) if state[item] == 0] 
        self.players = [1 , 2]
        self.current_player = current_player
        self.last_move = last_move

    def reset_board(self):
        self.state= {}
        for i in range(self.width * self.height):
            self.state[i] = 0
        self.available_state = np.zeros(self.width * self.height)
        self.available_state = [item for item in range(self.width * self.height)]
        self.current_player = 0
        self.last_move = -1

    def do_move(self , move):
        if move in self.available_state:
            self.state[move] = self.players[self.current_player]
            self.available_state.remove(move)
            self.last_move = move
            self.current_player = 0 if self.current_player == 1 else 1
        else:
            print("This Move Already Done")
            # raise Exception("This Move Already Done")

    
    def get_current_player(self):
        return self.current_player+1
        

    def current_state(self):
        """
            Which return some hand crafted feature for neural network
                1) position of first player with     [1 , 0 , 0 , 0 , 1]  "STATE PLAYER 1"
                2) position of second player with    [0 , 1 , 1 , 0 , 0]  "STATE PLAYER 2"
                3) position of which moved last done [0 , 0 , 1 , 0 , 0]  "last move done which position"
                4) Indicate which player move next   [0 , 0 , 0 , 0 , 0]  "player 1 : 0 , player 2: 1"
        """

        square_matrix = np.zeros((4 , self.width , self.height))

        for each_box in self.state:
            if each_box not in self.available_state:
                x =  each_box // self.width
                y =  each_box % self.height
                square_matrix[0][x][y] = 1.0 if self.state[each_box] == self.players[0] else 0.0
                square_matrix[1][x][y] = 1.0 if self.state[each_box] == self.players[1] else 0.0
        
        square_matrix[2][self.last_move//self.width][self.last_move%self.height] = 1.0
        
        if len(self.available_state) % 2 == 0:
            square_matrix[3][:][:] = 1.0
        
        # return square_matrix
        return square_matrix[: , ::-1 , :]
        # square_matrix[2][self.last_move//]

    def has_a_winner(self , with_player = 0):
        if len( self.state ) >= self.n_match:
            n = self.n_match
            for each_node in self.state:
                if each_node not in self.available_state:

                    c = each_node % self.width
                    r = each_node // self.height
                    
                    if(c < self.width - n + 1 and len(set([self.state[r * self.width + i] for i in range(c, c+n)])) == 1):
                        # print("---")
                        return (True, self.state[each_node]) if with_player else True

                    if(r < self.height - n + 1 and len(set([self.state[i * self.width + c] for i in range(r, r+n)])) == 1):
                        # print("|")
                        return (True, self.state[each_node]) if with_player else True

                    if(c <= self.width - n and r < self.height - n + 1 and len(set([self.state[i] for i in range(each_node, each_node + (n) * self.width, self.width + 1)])) == 1):
                        # print("\\", "why")
                        return (True, self.state[each_node]) if with_player else True

                    if(c >= n - 1 and r < self.height - n + 1 and len(set([self.state[i] for i in range(each_node, each_node + (n-1) * self.width, self.width - 1)])) == 1):
                        # print("/", "why", n)
                        # print([[self.state[i], i] for i in range(
                        #     each_node, each_node + n * self.width - n, self.width - 1)])
                        return (True, self.state[each_node]) if with_player else True
        return False , -1

    def has_a_winner_copy(self, with_player=0):
        if len(self.state) >= self.n_match:
            n = self.n_match
            for each_node in self.state:
                if each_node not in self.available_state:

                    c = each_node % self.width
                    r = each_node // self.height

                    if(c < self.width - n + 1 and len(set([self.state[r * self.width + i] for i in range(c, c+n)])) == 1):
                        print("---")
                        return (True, self.state[each_node]) if with_player else True

                    if(r < self.height - n + 1 and len(set([self.state[i * self.width + c] for i in range(r, r+n)])) == 1):
                        print("|")
                        return (True, self.state[each_node]) if with_player else True

                    if(c <= self.width - n  and r < self.height - n + 1 and len(set([self.state[i] for i in range(each_node, each_node + (n) * self.width , self.width + 1)])) == 1):
                        print("\\")
                        print([[self.state[i] , i] for i in range(
                            each_node, each_node + (n-1) * self.width, self.width + 1)])
                        return (True, self.state[each_node]) if with_player else True

                    if(c >= n - 1 and r < self.height - n + 1 and len(set([self.state[i] for i in range(each_node, each_node + (n-1) * self.width, self.width - 1)])) == 1):
                        print("/")
                        # print([[self.state[i] , i] for i in range(each_node, each_node + n * self.width - n, self.width - 1)])
                        return (True, self.state[each_node]) if with_player else True
        return False, -1
    def end_game(self , with_player = 0):
        if len(self.available_state)!=0:
            return self.has_a_winner(with_player)
        else:
            if with_player:
                return self.has_a_winner(1) if self.has_a_winner(1)[1] == 1 else (True , -1)
                # return self.has_a_winner(1) if self.has_a_winner(1)[1] == 1 else (True , 0)
            else:
                return True

    def graphic_display(self , player_1 = 1 , player_2 = 2):
        player_1_symbole = "O"
        player_2_symbole = "X"

        print("\n")
        for i in range(self.height):
            print("{:>45}".format("") , end="")
            for j in range(self.width):
                disp_symbol = "-"
                if self.state[i * self.height + j] != 0:
                    disp_symbol = player_1_symbole if self.state[i * self.height + j] == player_1 else player_2_symbole
               
                print("{:^4}".format(disp_symbol) , end="")

            print("" , end="\n")
        print("\n")
        

# class Game:
#     def __init__(self , width , height , number_match):
#         self.board = Board(width , height , number_match)  

    # def self_play_genrate_data(self):
        """This function use to genrate data for learning"""      


# b = Board(4, 4, 3, False,  [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0] , 0 , 8)
# b = Board(5 , 5 , 4)
# """ b.do_move(18)
# b.do_move(3)
# b.do_move(7)
# b.do_move(6)
# b.do_move(6+5)
# b.do_move(13)
# b.do_move(12)
# b.do_move(16)
# b.do_move(15)
# # b.do_move(18)
# b.do_move(17)
# b.do_move(19) """
# b.do_move(2)
# b.do_move(6)
# b.do_move(5)
# b.do_move(12)
# b.do_move(15)
# b.do_move(18)
# b.graphic_display()
# # print(b.available_state)
# print(b.has_a_winner_copy())

""""
# board.do_move(7)
# board.do_move(9)
1
# board.do_move(0)
# board.do_move(6)
# board.do_move(12 + 5)
# board.do_move(18 + 5)
# board.do_move(24 + 5)
# board.do_move(30 + 5)

# board.do_move(0)
# board.do_move(7)
# board.do_move(14)
# board.do_move(21)

board.do_move(3 + 1)
board.do_move(8 + 1)
board.do_move(13 + 1)
board.do_move(18 + 1)


board.current_player = 1

board.do_move(0)
board.do_move(7)
board.do_move(14)
board.do_move(21)
# print(board.state)

# board.graphic_display()
# print(board.current_state())
# board.do_move(5)
# print(board.state[4] == None)
print(board.end_game(1))

# print(board.available_state)
# print(board.state) """


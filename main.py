""" Implementation of a GUI TicTacToe with a KI player utilizing the minimax algorithm """

from tkinter import Canvas
import numpy as np
import tkinter as tk
import tkinter.font as TkFont
import math

class Player:
    """ class of human player

    """
    def __init__(self, name):
        self.name = name
        self.score = 0
    
    def add_score(self):
        """ updates score
        
        """
        self.score += 1


class KI:
    """ class of KI player
    
    """
    def __init__(self, name):
        self.name = name
        self.score = 0
    
    def add_score(self):
        """ updates score

        """
        self.score += 1


class Game:
    """ main game class
    
    """
    def __init__(self):
        self.window = tk.Tk()
        self.players = []
        self.window.title("Tic Tac Toe")
        self.canvas = Canvas(self.window, width=600, height=800)
        self.canvas.pack()
        self.logical_board = np.array([[0,0,0],[0,0,0],[0,0,0]])
        self.canvas.bind('<Button-1>', self.player_clicks)
        self.win_cond = [{(0,0), (0,1), (0,2)}, {(1,0), (1,1), (1,2)}, {(2,0), (2,1), (2,2)}, {(0,0), (1,0), (2,0)}, 
                        {(0,1), (1,1), (2,1)}, {(0,2), (1,2), (2,2)}, {(0,0), (1,1), (2,2)}, {(0,2), (1,1), (2,0)}]
        self.player = Player("Human")
        self.ki = KI("KI")
        self.font = TkFont.Font(family='Helvetica',size=36, weight='bold')
        self.current_winner = None
        self.initialize_board()

    def mainloop(self):
        """ mainloop for the application window
        
        """
        self.window.mainloop()
    
    def initialize_board(self):
        """ initializes the board by creating the grid and text
        
        """
        self.canvas.create_line((200,0), (200,600))
        self.canvas.create_line((400,0), (400,600))
        self.canvas.create_line((0,200), (600,200))
        self.canvas.create_line((0,400), (600,400))
        self.canvas.create_text((150, 650), font="bold 15", fill='#000000', text="\nYou have won {} times\nThe {} has won {} times".format(self.player.score, self.ki.name, self.ki.score), tags="score_mes")
        leave = self.canvas.create_text((400, 650), font="bold 15", fill='#880808', text="Quit the game")
        self.canvas.tag_bind(leave, "<Button-1>", lambda x: quit())

    
    def restart(self):
        """ resets the game state to allow for another round
        
        """
        self.canvas.delete("all")
        self.logical_board = np.array([[0,0,0],[0,0,0],[0,0,0]])
        self.current_winner = None
        self.initialize_board()
        
    def update_score(self):
        """ updates displayed messages after game
        
        """
        self.canvas.delete("score_mes")
        self.canvas.create_text((150, 650), font="bold 15", fill='#000000', text="\nYou have won {} times\nThe {} has won {} times".format(self.player.score, self.ki.name, self.ki.score), tags="score_mes")
        id = self.canvas.create_text((400, 650), font="bold 15", fill='#880808', text="Quit the game")
        self.canvas.tag_bind(id, "<Button-1>", lambda x: quit())
        restart = self.canvas.create_text((400, 675), font="bold 15", fill='#880808', text="Play again!")
        self.canvas.tag_bind(restart, "<Button-1>", lambda x: self.restart())

    def convert_board_to_logical(self, board_pos):
        """ converts the clicked position to fit numpy array coordinates

        Args:
            board_pos (array): x and y coordinates of mouse click on user interface

        Returns:
            array: contains the coordinates for the numpy array
        """
        x_coord = int(board_pos[0] / 200)
        y_coord = int(board_pos[1] / 200)
        return [x_coord, y_coord]
    
    def convert_logical_to_board(self, logical_pos):
        """ converts numpy array coordinates to allow for drawing in user interface

        Args:
            logical_pos (array): contains the coordinates for the numpy array

        Returns:
            [array]: x and y coordinates for user interface
        """
        return [logical_pos[0] * 200, logical_pos[1] * 200]

    def check_logical_pos(self, logical_pos):
        """ checks if grid occupied

        Args:
            logical_pos (array): coordinates of click

        Returns:
            Bool: True if click allowed, else False
        """
        if self.logical_board[logical_pos[0]][logical_pos[1]] == 0:
            self.logical_board[logical_pos[0]][logical_pos[1]] = 1
            return True
        else:
            return False
    
    def draw_x(self, board_pos):
        """ draws an X on the user interface

        Args:
            board_pos (array): coordinates for drawing
        """
        self.canvas.create_line((board_pos[0]+50, board_pos[1]+50), (board_pos[0]+150, board_pos[1]+150), width = 20, fill = "green")
        self.canvas.create_line((board_pos[0]+150, board_pos[1]+50), (board_pos[0]+50, board_pos[1]+150), width = 20, fill = "green")
    
    def draw_o(self, board_pos):
        """ draws an O on the user interface

        Args:
            board_pos (array): coordinates for drawing
        """
        self.canvas.create_oval((board_pos[0]+50, board_pos[1]+50), (board_pos[0]+150, board_pos[1]+150), width = 20, outline = "red")
    
    def check_player_winner(self):
        """ checks if player has won

        Returns:
            Bool: True if player has won, False otherwise
        """
        x = np.argwhere(self.logical_board == 1)
        x_marked = set()
        for i in x:
            x_marked.add((i[0], i[1]))
        for sub in self.win_cond:
            if sub.issubset(x_marked):
                self.current_winner = 1
                return True
        return False
    
    def check_ki_winner(self):
        """checks if ki has won

        Returns:
            Bool: True if player has won, False otherwise
        """
        o = np.argwhere(self.logical_board == -1)
        o_marked = set()
        for j in o:
            o_marked.add((j[0], j[1]))
        for sub in self.win_cond:
            if sub.issubset(o_marked):
                self.current_winner = -1
                return True
        return False
    
    def check_draw(self):
        """checks if game is drawn

        Returns:
            Bool: True if player has won, False otherwise
        """
        free = np.argwhere(self.logical_board == 0)
        if len(free) == 0:
            self.current_winner = 0
            return True
        return False

    def player_clicks(self, event):
        """ allows player to select field, triggered by left mouse click

        Args:
            event (Click)
        """
        board_pos = [event.x, event.y]
        if event.y < 600:
            logical_pos = self.convert_board_to_logical(board_pos)
            if self.check_logical_pos(logical_pos):
                board_pos = self.convert_logical_to_board(logical_pos)
                self.draw_x(board_pos)
                if self.check_player_winner():
                    self.player.add_score()
                    self.update_score()
                    self.logical_board = np.array([[1,1,1],[1,1,1],[1,1,1]])  # player can't click on board until game is restarted
                elif self.check_draw():
                    self.player.add_score()
                    self.ki.add_score()
                    self.update_score()
                else:
                    self.computer_plays()
            
    def computer_plays(self):
        """ main function of the ki
        
        """
        choice = self.minimax()
        print(choice)
        choice = choice["position"]
        board_pos = self.convert_logical_to_board(choice)
        self.logical_board[choice[0]][choice[1]] = -1
        self.draw_o(board_pos)
        if self.check_ki_winner():
            self.ki.add_score()
            self.update_score()
            self.logical_board = np.array([[1,1,1],[1,1,1],[1,1,1]])
        elif self.check_draw():
            self.player.add_score()
            self.ki.add_score()
            self.update_score()
    
    def minimax(self, player=None):
        """ minimax algorithm for the ki player

        Args:
            player (int): -1 for minimizer, 1 for maximizer. Defaults to None for first function call.

        Returns:
            [dictionary]: containing the array position of the optimal move and the calculated score
        """
        human_player = 1
        ki_player = -1
        if player is None:
            player = ki_player
        if self.current_winner == -1*(player):
            return {"position": None, "score": 1 if (-1*(player)) == human_player else -1}
        elif self.current_winner == 0:
            return {"position": None, "score": 0}
        if player == ki_player:
            best_move = {"position": None, "score": math.inf}
        else:
            best_move = {"position": None, "score": -math.inf}
        free = np.argwhere(self.logical_board == 0)
        available_choices = [x for x in range(len(free))]
        for choice in available_choices:
            chosen_field = free[choice]
            self.minimax_move(chosen_field, player)
            simulation_score = self.minimax(-1*(player))
            self.logical_board[chosen_field[0]][chosen_field[1]] = 0
            self.current_winner = None
            simulation_score["position"] = chosen_field
            if player == human_player:
                if simulation_score["score"] > best_move["score"]:
                    best_move = simulation_score
            else:
                if simulation_score["score"] < best_move["score"]:
                    best_move = simulation_score
        return best_move

    def minimax_move(self, field, player):
        """ helper function for self.minimax()

        Args:
            field (array): coordinates for numpy array
            player (int): defines maximizer and minimizer
        """
        if player == -1:
            self.logical_board[field[0]][field[1]] = -1
        else:
            self.logical_board[field[0]][field[1]] = 1
        self.check_player_winner()
        self.check_ki_winner()
        self.check_draw()


def main():
    """ starts the application
    
    """
    game = Game()
    game.mainloop()


if __name__ == "__main__":
    main()

class TicTacToe():
    """
        This module allows user to create a simple TicTacToe enviorment for their use.
        
        Attributes:
            board(list): list of 9 element traking the status of the board 
            winner(str): traking the name of the winner
            player_1_turn(bool): priorty bit to keep track of player order
            player_1(str): name of player 1
            player_2(str):name of player 2
    """
    def __init__(self, player_1:str="player_1",player_2:str="player_2"):
        """
            Creates the TicTacToe object

            Parameters:
                player_1 (str): name of the first player (default:player_1)
                player_2 (str): name of the second player (default:player_2)
        """
        self.board = ['1','2','3','4','5','6','7','8','9']
        self.winner = ""
        self.player_1_turn = True
        self.player_1 = player_1 
        self.player_2 = player_2

    def get_winner(self):
        """
            Grabs the name of the winner

            Returns:
                str: name of the winner
        """
        return self.winner

    def can_play(self):
        """
            Check if there are move to be played

            Returns:
                bool: is the spot available to play
        """
        board = self.board
        for i, char in enumerate(board):
            if(char == i+1):
                return True
        return False
    
    def get_board(self):
        """
            Creates a printable string representing board 
            Returns:
                str: string representation of the board
        """
        output = "|{0}|{1}|{2}|\n-------\n"\
            "|{3}|{4}|{5}|\n-------\n"\
            "|{6}|{7}|{8}|\n".format(*self.board)
        return output

    def play_turn(self, spot:int=0):
        """
            Perameters:
                spot(int): stop on the board to fill
            Returns:
                int:
                    +1  : game has ended
                    +0  : successful in placing the spot
                    -1 : filled spot was selected
        """
        val = 0
        if (spot>0 and spot<10 and self.board[spot-1].isdigit()):
            char = "o"
            if(self.player_1_turn):
                char = "x"
                self.player_1_turn = False
            else: self.player_1_turn = True
            self.board[spot-1] = char
            val = 0
        else: 
            val = -1
        if(self.check_winner() or self.can_play()):
            val = 1
        return val
    
    def char_to_player(self, char):
        """
            Gives the name of the player from the character

            Retures:
                str: name of the player associated with the character
        """
        player = self.player_1
        if char =='o':
            player = self.player_2
        return player

    def check_winner(self):
        """
            Check if ther is winner and update the board if there is one

            Returns:
                bool: true if we have a winner and false no winner
        """
        output = False
        char = '-'
        if (self.board[4] != 5):
            char = self.board[4]
            # diagonal case
            if (char == self.board[0] and char == self.board[8]):
                self.board[4], self.board[0], self.board[8] = '\\','\\','\\'
                output = True
            elif (char == self.board[2] and char == self.board[6]):
                self.board[4], self.board[2], self.board[6] = '/','/','/'
                output = True
            # horizontal case
            elif (char == self.board[3] and char == self.board[5]):
                self.board[4], self.board[3], self.board[5] = '-','-','-'
                output = True
            # vertical case
            elif (char == self.board[1] and char == self.board[7]):
                self.board[4], self.board[1], self.board[7] = '|','|','|'
                output = True
        if(self.board[0] !=1 and not output):
            char = self.board[0]
            #horizontal case
            if (char == self.board[2] and self.board[1] == char):
                self.board[0], self.board[1], self.board[2] = '-','-','-'  
                output = True
            #vertical case
            elif (char == self.board[3] and char == self.board[6]): 
                self.board[0], self.board[3], self.board[6] = '|','|','|'
                output = True     
        if(self.board[8] != 9 and not output):
            char = self.board[8]
            #horizontal case
            if (self.board[6] == char and self.board[7] == char):
                self.board[6], self.board[7], self.board[8] = '-','-','-'
                output = True
            #vertical case
            elif (self.board[2] == char and self.board[5] == char): 
                self.board[2], self.board[5], self.board[8] = '|', '|', '|'
                output = True
        if (output):
            self.winner = self.char_to_player(char)
        return output
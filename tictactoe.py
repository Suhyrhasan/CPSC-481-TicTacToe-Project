import copy
import sys
import pygame
import random
import numpy as np

from constants import *

# --- PYGAME SETUP ---

pygame.init()
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption('TIC TAC TOE - CPSC 481')
screen.fill( BG_COLOR )

# --- CLASSES ---


class Board:

    # This is where the board gets initialized/created. Because its a tic tac toe, we use 
    # a 2D array and set the places where we can play/mark to 0, Everywhere else
    # on the board where a player should not make a move is left EMPTY
    def __init__(self):
        #self.squares = np.zeros( (ROWS, COLS) )
        arr = np.empty(shape=(ROWS,COLS), dtype='object')
        arr[0,2] = 0

        arr[1,1] = 0
        arr[1,2] = 0
        arr[1,3] = 0

        arr[2,0] = 0
        arr[2,1] = 0
        arr[2,2] = 0
        arr[2,3] = 0
        arr[2,4] = 0
        self.squares = arr
        print(self.squares)
        self.empty_sqrs = self.squares # [squares]
        self.marked_sqrs = 0

    def final_state(self, show=False):
        # Returns 0 if there is no winner so keeps the board empty and the game going
        '''
            @return 0 if there is no win yet
            @return 1 if player 1 wins
            @return 2 if player 2 wins
        '''

        # vertical wins
        # This for-loop checks vertical wins which is just at the middle of the pyramid
        # line 53 checks specifically any column and rows 0 1 2
        # The second if "show" happens when a player wins with a vertical win. This just 
        # determines the color of the line that crosses the winning move
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show: 
                    color = CIRC_COLOR if self.squares[0][col] == 2 else CROSS_COLOR # Choose color of the line based on the winner
                    iPos = (col * SQSIZE + SQSIZE // 2, 20) # This sets the starting point of the cross line
                    fPos = (col * SQSIZE + SQSIZE // 2, HEIGHT - 20) # This sets the ending point of the cross line
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH) # Draws the line using initial and final position
                return self.squares[0][col] 

        # horizontal wins
        # Because there are more columns wins and the 3rd row has multiple possible sets to win
        # each if condition is for each possibile win options. The show is similar to verticle win
        for row in range(ROWS):
            if self.squares[1][1] == self.squares[1][2] == self.squares[1][3] != 0:
                if show:
                    color = CIRC_COLOR if self.squares[1][0] == 2 else CROSS_COLOR
                    iPos = (200 + 20, SQSIZE + SQSIZE // 2)
                    fPos = (800 - 20, SQSIZE + SQSIZE // 2)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[1][0]
            elif (self.squares[2][0] == self.squares[2][1] == self.squares[2][2] != 0):
                if show:
                    color = CIRC_COLOR if self.squares[2][0] == 2 else CROSS_COLOR
                    iPos = (20, 2 * SQSIZE + SQSIZE // 2)
                    fPos = (600 - 20, 2 * SQSIZE + SQSIZE // 2)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[2][0]
            elif (self.squares[2][1] == self.squares[2][2] == self.squares[2][3] != 0):
                if show:
                    color = CIRC_COLOR if self.squares[2][1] == 2 else CROSS_COLOR
                    iPos = (200 + 20, 2 * SQSIZE + SQSIZE // 2)
                    fPos = (800 - 20, 2 * SQSIZE + SQSIZE // 2)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[2][0]
            elif (self.squares[2][2] == self.squares[2][3] == self.squares[2][4] != 0):
                if show:
                    color = CIRC_COLOR if self.squares[2][2] == 2 else CROSS_COLOR
                    iPos = (400 + 20 , 2 * SQSIZE + SQSIZE // 2)
                    fPos = (WIDTH - 20, 2 * SQSIZE + SQSIZE // 2)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[2][0]

        # desc diagonal
        # Checks if the diagonal wins from the top of the pyramid to the bottom RIGHT
        if self.squares[0][2] == self.squares[1][3] == self.squares[2][4] != 0:
            if show:
                color = CIRC_COLOR if self.squares[1][3] == 2 else CROSS_COLOR
                iPos = (1000 - 20, HEIGHT - 20)
                fPos = (400 + 20, 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]

        # asc diagonal
        # Checks if the diagonal wins from the top of the pyramid to the bottom LEFT
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (20, HEIGHT - 20)
                fPos = (600 - 20, 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]

        # no win yet
        return 0

    # Everytime a player makes a move, it replaces the 0 on the board with the player 1 or 
    # player 2 value so replaces 0 with 1 or 2.
    # there is only 9 spaces so this is a way to verify if all possible moves are made
    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    # Check if the specific square is empty, So it will return true if the square
    # is empty.
    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0

    # Returns all the empty squares in the map. This is used to see where the next moves
    # can be marked. Its a way of updating the board
    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row, col):
                    empty_sqrs.append( (row, col) )
        
        return empty_sqrs

    # Checks if the boardgame is full since there are only 9 spaces to populate
    def isfull(self):
        return self.marked_sqrs == 9

    # Checks if the board is empty, not just a specific square
    def isempty(self):
        return self.marked_sqrs == 0

class AI:

    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

    # --- RANDOM ---

    def rnd(self, board):
        empty_sqrs = board.get_empty_sqrs()
        idx = random.randrange(0, len(empty_sqrs))

        return empty_sqrs[idx] # (row, col)

    # --- MINIMAX ---

    def minimax(self, board, maximizing):
        
        # terminal case
        case = board.final_state()

        # player 1 wins
        if case == 1:
            return 1, None # eval, move

        # player 2 wins
        if case == 2:
            return -1, None

        # draw
        elif board.isfull():
            return 0, None

        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move

    # --- MAIN EVAL ---

    def eval(self, main_board):
        if self.level == 0:
            # random choice
            eval = 'random'
            move = self.rnd(main_board)
        else:
            # minimax algo choice
            eval, move = self.minimax(main_board, False)

        print(f'AI has chosen to mark the square in pos {move} with an eval of: {eval}')

        return move # row, col

class Game:

    # Everything gets initialized here
    def __init__(self):
        self.board = Board() # Create board
        self.ai = AI()  # Setup AI
        self.player = 1   #1-cross  #2-circles also this is the value of the player when marking
        self.gamemode = 'ai' # pvp or ai
        self.running = True
        self.show_lines()

    # --- DRAW METHODS ---

    def show_lines(self):
        # back ground color
        screen.fill( BG_COLOR )

        # vertical
        # This is where we can draw the line for the game. I created a 4 verticle lines for rows
        pygame.draw.line(screen, LINE_COLOR, (200, 200), (200, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (400, 0), (400, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (600, 0), (600, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (800, 200), (800, HEIGHT), LINE_WIDTH)

        # horizontal
        # 2 Horizontal lines for column making it a 3X5
        pygame.draw.line(screen, LINE_COLOR, (200, SQSIZE), (800, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - SQSIZE), (WIDTH, HEIGHT - SQSIZE), LINE_WIDTH)
        

    def draw_fig(self, row, col):

        # Draw two lines to make X. These attributes are referenced on constrant.py
        if self.player == 1:
            # draw cross
            # desc line
            start_desc = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
            end_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
            # asc line
            start_asc = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            end_asc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)
        
        # Draw circle
        elif self.player == 2:
            # draw circle
            center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
            pygame.draw.circle(screen, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)

    # --- OTHER METHODS ---

    def make_move(self, row, col):
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()

    def next_turn(self):
        self.player = self.player % 2 + 1

    def change_gamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'

    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.isfull()

    def reset(self):
        self.__init__()

def main():

    # --- OBJECTS ---

    game = Game()
    board = game.board
    ai = game.ai

    # --- MAINLOOP ---

    while True:
        
        # pygame events
        for event in pygame.event.get():

            # quit event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # keydown event
            if event.type == pygame.KEYDOWN:

                # g-gamemode
                if event.key == pygame.K_g:
                    game.change_gamemode()

                # r-restart
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai

                # 0-random ai
                if event.key == pygame.K_0:
                    ai.level = 0
                
                # 1-random ai
                if event.key == pygame.K_1:
                    ai.level = 1

            # click event
            # This converts pixels to rows and colums. In a tradition tictactoe if you clicked 
            # the first top left square, it will display (0,300) where 300 is the length of the
            # square but this allows it to set the click to (0,0) which converted pixel
            # row and col 
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQSIZE
                col = pos[0] // SQSIZE
                
                # human mark sqr
                # This calls empty squre to check if its empty or not and make a move based
                # on the return value. This is referencing line 127
                if board.empty_sqr(row, col) and game.running:
                    game.make_move(row, col)

                    if game.isover():
                        game.running = False


        # AI initial call
        if game.gamemode == 'ai' and game.player == ai.player and game.running:

            # update the screen
            pygame.display.update()

            # eval
            row, col = ai.eval(board)
            game.make_move(row, col)

            if game.isover():
                game.running = False
            
        pygame.display.update()
        
main()
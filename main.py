try:
    import pygame_sdl2
    pygame_sdl2.import_as_pygame()
except ImportError:
    pass
import pygame
import random
from typing import Tuple, Any
import numpy as np
import sys
import pygame_menu


class Game:
    def __init__(self):
        # SET CONSTANTS
        pygame.init()
        self.GAME_MODE = 0
        self.WIDTH = 600
        self.HEIGHT = 600
        self.COLOR = '#04293A'
        self.COLOR_B = (50, 5, 20)
        self.BOARD_ROWS = 3
        self.BOARD_COLS = 3
        self.bg = pygame.image.load("images/bg.png")
        self.x = pygame.image.load('images/x2.png')
        self.o = pygame.image.load('images/o2.png')
        self.game_over = False
        # SET SCREEN
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Tic Tac Toe')
        self.screen.blit(self.bg, (0, 0))

        # BOARD
        self.board = np.zeros((self.BOARD_ROWS, self.BOARD_COLS))

    def set_difficulty(self, selected: Tuple, value: Any) -> None:
        # Set the difficulty of the game.
        self.GAME_MODE = value

    def draw_lines(self):
        # HORIZONTAL LINES
        pygame.draw.rect(self.screen, self.COLOR_B, pygame.Rect(200, 10, 10, 580), 5, 4)
        pygame.draw.rect(self.screen, self.COLOR_B, pygame.Rect(400, 10, 10, 580), 5, 4)
        # VERTICAL LINES
        pygame.draw.rect(self.screen, self.COLOR_B, pygame.Rect(10, 400, 580, 10), 5, 4)
        pygame.draw.rect(self.screen, self.COLOR_B, pygame.Rect(10, 200, 580, 10), 5, 4)

    def draw_figures(self):
        # draw figures in position
        for row in range(self.BOARD_ROWS):
            for col in range(self.BOARD_COLS):
                if self.board[row, col] == 1:
                    self.screen.blit(self.x, (int(col * 200 + 50), int(row * 200 + 50)))
                if self.board[row, col] == 2:
                    self.screen.blit(self.o, (int(col * 200 + 50), int(row * 200 + 50)))

    # Change numbers on the board
    def mark_square(self, row, col, player):
        self.board[row, col] = player

    # return True if have available square(0 is available, 1 or 2(player) is not available)
    def available_square(self, row, col):
        return self.board[row, col] == 0

    # return a list of all available squares in format:(row, col)
    def get_empty_sqr(self):
        sqrs = []
        for i in range(self.BOARD_ROWS):
            for y in range(self.BOARD_COLS):
                if self.available_square(i, y):
                    sqrs.append((i, y))
        return sqrs

    # a random ai player
    def ai_player(self, player):
        pygame.time.wait(1000)
        empty_sqrs = self.get_empty_sqr()
        rand = random.randrange(0, len(empty_sqrs))
        row = empty_sqrs[rand][0]
        col = empty_sqrs[rand][1]
        self.mark_square(row, col, player)
        self.draw_figures()
        pygame.mixer.music.load("sound_effects/place2.mp3")
        pygame.mixer.music.play(loops=0)

    # return True, if the board is full
    def is_board_full(self):
        if 0 in self.board:
            return False
        else:
            return True

    # check all possible winning positions
    def check_win(self, player):
        for i in range(self.BOARD_COLS):
            # vertical check
            if self.board[0, i] == player and self.board[1, i] == player and self.board[2, i] == player:
                self.draw_vertical_winning_line(i, player)

                return True
            # horizontal check
            if self.board[i, 0] == player and self.board[i, 1] == player and self.board[i, 2] == player:
                self.draw_horizontal_winning_line(i, player)

                return True
        # desc check
        if self.board[0, 0] == player and self.board[1, 1] == player and self.board[2, 2] == player:
            self.draw_desc_winning_line(player)
            return True
        # asc check
        if self.board[0, 2] == player and self.board[1, 1] == player and self.board[2, 0] == player:
            self.draw_asc_winning_line(player)
            return True
        return False

    # draw vertical line
    def draw_vertical_winning_line(self, col, player):
        color = ''
        pos_x = col * 200 + 105
        if player == 1:
            color = self.COLOR
        elif player == 2:
            color = self.COLOR
        pygame.draw.line(self.screen, color, (pos_x, 15), (pos_x, 585), 15)

    # draw horizontal line
    def draw_horizontal_winning_line(self, row, player):
        color = ''
        pos_y = row * 200 + 105
        if player == 1:
            color = self.COLOR
        elif player == 2:
            color = self.COLOR
        pygame.draw.line(self.screen, color, (15, pos_y), (585, pos_y), 15)

    # draw asc line
    def draw_asc_winning_line(self, player):
        color = ''
        if player == 1:
            color = self.COLOR
        elif player == 2:
            color = self.COLOR
        pygame.draw.line(self.screen, color, (582, 32), (32, 582), 15)

    # draw desc line
    def draw_desc_winning_line(self, player):
        color = ''
        if player == 1:
            color = self.COLOR
        elif player == 2:
            color = self.COLOR
        pygame.draw.line(self.screen, color, (30, 30), (570, 570), 15)

    # restart the game
    def restart(self):
        self.screen.blit(self.bg, (0, 0))
        self.draw_lines()
        for i in range(self.BOARD_COLS):
            for y in range(self.BOARD_ROWS):
                self.board[i, y] = 0
        self.game_over = False

    # the main game function
    def main(self):
        # set screen, lines, and player 1
        self.screen.blit(self.bg, (0, 0))
        self.draw_lines()
        player = 1
        while True:
            if not self.game_over:
                # if gamemode is 2, the ai player is active
                if player == self.GAME_MODE:
                    self.ai_player(player)
                    if self.check_win(player):
                        self.draw_figures()
                        self.check_win(player)
                        self.game_over = True
                    else:
                        # change player
                        player = player % 2 + 1
            # set click events
            for event in pygame.event.get():
                self.draw_figures()
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                    mouse_x = event.pos[0]
                    mouse_y = event.pos[1]

                    clicked_row = int(mouse_y // 200)
                    clicked_col = int(mouse_x // 200)
                    if self.available_square(clicked_row, clicked_col):
                        self.mark_square(clicked_row, clicked_col, player)
                        if self.check_win(player):
                            self.draw_figures()
                            self.check_win(player)
                            self.game_over = True
                        else:
                            player = player % 2 + 1
                            self.draw_figures()
                        # play sound when the player takes a step
                        pygame.mixer.music.load("sound_effects/place2.mp3")
                        pygame.mixer.music.play(loops=0)
                        if self.is_board_full():
                            self.game_over = True
                # restart key is R
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.restart()
            if self.game_over:
                pygame.display.update()
                pygame.mixer.music.load("sound_effects/victory.mp3")
                pygame.mixer.music.play(loops=0)
                pygame.time.wait(3000)
                Menu()

            pygame.display.update()


class Menu(Game):
    def __init__(self):
        super().__init__()
        # set GAME MENU
        self.surface = pygame.display.set_mode((600, 600))
        self.menu = pygame_menu.Menu('Tic Tac Toe', 600, 600,
                                     theme=pygame_menu.themes.THEME_ORANGE)
        self.menu.add.selector('Gamemode :', [('VS PLAYER', 0), ('VS COMPUTER', 2)], onchange=self.set_difficulty)
        self.menu.add.button('Play', self.main)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)
        self.menu.mainloop(self.surface)


# START THE GAME
start = Menu()

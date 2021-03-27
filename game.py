import pygame as pg
from os import getcwd
from board import Gameboard
import json


class Game():
    def __init__(self):
        pg.init()
        self.running, self.playing = True, False
        self.h, self.back, self.lshift, = False, False, False
        self.keydown, self.mousedown, self.mouseup = False, False, False
        self.key_num = None
        self.timer = 0
        self.WIDTH, self.HEIGHT = 725, 750
        self.WINDOW_RES = (self.WIDTH, self.HEIGHT)
        # self.display = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        self.WINDOW = pg.display.set_mode(self.WINDOW_RES)
        pg.display.set_caption("Sudoku")
        icon = pg.image.load(getcwd() + "\\icon.png")
        pg.display.set_icon(icon)
        self.gameboard = Gameboard()
        self.won = False
        self.BLACK, self.DARK_GRAY = (0, 0, 0), (75, 75, 75)
        self.WHITE = (255, 255, 255)
        self.L_GRAY = (180, 180, 180)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running, self.playing = False, False
            elif event.type == pg.KEYDOWN:
                self.keydown = True
                if event.key == pg.K_h:
                    self.h = True
                elif event.key == pg.K_BACKSPACE:
                    self.back = True
                elif event.mod and event.key == pg.KMOD_LSHIFT:
                    self.lshift = True
                else:
                    self.key = event.unicode
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.mousedown = True
            elif event.type == pg.MOUSEBUTTONUP:
                self.mouseup = True

    def reset_keys(self):
        self.h, self.back, self.lshift, = False, False, False
        self.keydown, self.mousedown, self.mouseup = False, False, False

    def draw_board(self):
        """
        Draws the gameboard on the game window
        """
        size = self.HEIGHT - 300
        pos = (int((self.WIDTH - size)/2), 25)
        self.gameboard.rect = pg.Rect(pos[0], pos[1], size, size)
        # draws lines
        for i in range(size//9, size-9, size//9):
            if i % 3 == 0:
                line_thickness = 2
            else:
                line_thickness = 1
            pg.draw.line(self.WINDOW, self.DARK_GRAY, (pos[0]+i, pos[1]),
                         (pos[0]+i, pos[1]+size), line_thickness)
            pg.draw.line(self.WINDOW, self.DARK_GRAY, (pos[0], pos[1]+i),
                         (pos[0]+size, pos[1]+i), line_thickness)
        # draws box
        pg.draw.rect(self.WINDOW, self.BLACK, self.gameboard.rect, 3)
        # draws numbers
        for row in range(9):
            for col in range(9):
                if self.gameboard.og_board[row][col] != 0:
                    font = pg.font.SysFont('segoeuisemibold', 36)
                else:
                    font = pg.font.SysFont('segoeui', 36)
                if self.gameboard.board[row][col] != 0:
                    num = font.render(str(self.gameboard.board[row][col]),
                                      True, self.BLACK)
                    self.WINDOW.blit(num, ((col*50)+pos[0]+16, (row*50)+pos[1]-2))

    def draw_button(self, x, y, w, h, text="", color=(180, 180, 180), font=25):
        """
        general function used to draw a button, returns the buttons rect object
        """
        button = pg.Rect(x, y, w, h)
        pg.draw.rect(self.WINDOW, (color[0]-50, color[1]-50, color[2]-50), button)
        pg.draw.rect(self.WINDOW, color, (x+2, y+2, w-4, h-4))
        text = pg.font.SysFont('ebrima', font).render(text, True, self.BLACK)
        text_pos = (x + (w//2) - (text.get_rect().w//2),
                    y + (h//2) - (text.get_rect().h//2))
        self.WINDOW.blit(text, text_pos)
        return button

    def save(self):
        data = json.load(open(getcwd() + "\\data.json"))
        data["og_gameboard"] = self.gameboard.og_board
        data["gameboard"] = self.gameboard.board
        data["time"] = pg.time.get_ticks()
        # change difficulty
        data["difficulty"] = 1
        outfile = open("data.json", "w")
        json.dump(data, outfile)
        outfile.close()

    def load(self):
        data = json.load(open(getcwd() + "\\data.json"))
        self.gameboard.og_board = data["og_gameboard"]
        self.gameboard.board = data["gameboard"]
        self.timer = data["time"]

    def show_time(self):
        time = (self.timer//1000)
        time_text = str(100 + time // 60)[1:3] + ":" + str(100 + time % 60)[1:3]
        text = pg.font.SysFont('ebrima', 25).render(time_text+str(), True,
                                                    self.BLACK)
        self.WINDOW.blit(text, ((self.WIDTH//2)-28, 625))

    def menu_loop(self):
        # draws menu screen
        self.WINDOW.fill(self.WHITE)
        text = pg.font.SysFont('ebrima', 70).render('Sudoku', True, self.BLACK)
        textRect = text.get_rect()
        self.WINDOW.blit(text, (self.WIDTH//2 - textRect.width//2,
                                self.HEIGHT//2 - ((textRect.height//2) + 180)))
        start_button = self.draw_button((self.WIDTH//2)-75, 300, 160, 60,
                                        "start", self.L_GRAY, 24)
        load_button = self.draw_button((self.WIDTH//2)-75, 400, 160, 60,
                                       "load save", self.L_GRAY, 24)
        # main loop
        while self.running:
            self.check_events()
            if self.mouseup:
                mouse_pos = pg.mouse.get_pos()
                if start_button.collidepoint(mouse_pos):
                    try:
                        self.gameboard.create_solution()
                        self.playing = True
                    except AttributeError:
                        pass
                elif load_button.collidepoint(mouse_pos):
                    self.load()
                    self.playing = True
            if self.playing:
                return
            self.reset_keys()
            pg.display.update()

    def game_loop(self):
        RED, YELLOW = (255, 25, 25), (255, 255, 120)
        col, row, size = 0, 0, self.HEIGHT - 300
        errors, notes = [], []
        won = False
        clock = pg.time.Clock()
        while self.playing:
            self.check_events()
            self.WINDOW.fill(self.WHITE)
            for pos in errors:
                pg.draw.rect(self.WINDOW, YELLOW, (50*pos[0]+137, 50*pos[1]+25,
                                                   50, 50))
            if won:
                rect = (int((self.WIDTH - size)/2), 25, size, size)
                pg.draw.rect(self.WINDOW, (150, 255, 150), rect)
                text = pg.font.SysFont('ebrima', 25).render("You Won!", True,
                                                            self.BLACK)
                self.WINDOW.blit(text, ((self.WIDTH//2)-45, 485))
            else:
                self.timer += clock.tick(30)
            self.draw_board()
            save_button = self.draw_button(215, 540, 145, 45, "save game")
            clear_button = self.draw_button(380, 540, 120, 45, "clear")
            exit_button = self.draw_button(25, 25, 86, 45, "exit")
            if self.mousedown:
                mouse_pos = pg.mouse.get_pos()
                if self.gameboard.rect.collidepoint(mouse_pos):
                    col = (mouse_pos[0]-137)//50
                    row = (mouse_pos[1]-25)//50
                elif save_button.collidepoint(mouse_pos):
                    self.save()
                elif clear_button.collidepoint(mouse_pos):
                    self.gameboard.clear()
                    errors = []
                elif exit_button.collidepoint(mouse_pos):
                    self.playing = False
            elif self.keydown and self.gameboard.og_board[row][col] == 0:
                if self.h:
                    self.gameboard.solve()
                    self.gameboard.empty_spaces = 0
                elif self.back and self.gameboard.board[row][col] != 0:
                    self.gameboard.board[row][col] = 0
                    self.gameboard.empty_spaces += 1
                else:
                    try:
                        num = int(self.key)
                        if self.lshift:
                            notes.append((row, col, num))
                        else:
                            if self.gameboard.board[row][col] == 0:
                                self.gameboard.empty_spaces -= 1
                            self.gameboard.board[row][col] = num
                    except Exception:
                        pass
                errors = self.gameboard.check()
                if len(errors) == 0 and self.gameboard.empty_spaces == 0:
                    won = True
            # draws a red square around selected cell on the gameboard
            pg.draw.rect(self.WINDOW, RED, (50*col+137, 50*row+25, 50, 50), 3)
            self.show_time()
            self.reset_keys()
            pg.display.update()

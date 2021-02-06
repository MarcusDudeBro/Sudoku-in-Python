import pygame as pg
import os
import json
import copy
import random
from tree import Tree

# Game Window Initialization--------------
WIDTH, HEIGHT = 725, 750
WINDOW_RES = (WIDTH, HEIGHT)
pg.init()
WINDOW = pg.display.set_mode(WINDOW_RES)
pg.display.set_caption("Sudoku")
# colors----------------------------------
BLACK = (0, 0, 0)
DARK_GRAY = (75, 75, 75)
LIGHT_GRAY = (180, 180, 180)
WHITE = (255, 255, 255)
RED = (255, 25, 25)
YELLOW = (255, 255, 120)
# other constants-------------------------
PATH = os.getcwd()
CLOCK = pg.time.Clock()
size = HEIGHT - 300
icon = pg.image.load(PATH + "\\icon.png")
pg.display.set_icon(icon)


def check_board(board):
    """ checks if there are any errors on a gameboard
    return(errors): returns true if there are errors and false otherwise
    """
    errors = []
    # check horizontals
    for i in range(9):
        number_pos = [[] for k in range(9)]
        for j in range(9):
            if board[i][j] != 0:
                number_pos[board[i][j]-1].append((j, i))
        for positions in number_pos:
            if len(positions) > 1:
                for pos in positions:
                    errors.append(pos)
        # check verticals
        number_pos = [[] for k in range(9)]
        for j in range(9):
            if board[j][i] != 0:
                number_pos[board[j][i]-1].append((i, j))
        for positions in number_pos:
            if len(positions) > 1:
                for pos in positions:
                    errors.append(pos)
        # check boxes
        number_pos = [[] for k in range(9)]
        for row in range(i//3 * 3, i//3 * 3 + 3):
            for col in range(i % 3 * 3, i % 3 * 3 + 3):
                if board[row][col] != 0:
                    number_pos[board[row][col]-1].append((col, row))
        for positions in number_pos:
            if len(positions) > 1:
                for pos in positions:
                    errors.append(pos)
    return errors


def remove_candidates(candidates, number):
    try:
        candidates.remove(number)
    except ValueError:
        pass


def create_solution():
    empty_spaces = 0
    gameboard = [[0]*9 for i in range(9)]
    tree = Tree()
    for row in range(9):
        previous = tree.add_root(None)
        col = 0
        while col < 9:
            if tree.children(previous) is None:
                candidates = [i for i in range(1, 10)]
                for i in range(0, col):
                    remove_candidates(candidates, gameboard[row][i])
                for i in range(0, row):
                    remove_candidates(candidates, gameboard[i][col])
                for i in range(row//3 * 3, row):
                    for j in range(col//3 * 3, col//3 * 3 + 3):
                        remove_candidates(candidates, gameboard[i][j])
                tree.add_children(previous, candidates)
            if len(tree.children(previous)) == 0:
                tree.remove(previous)
                previous = tree.parent(previous)
                col -= 1
                gameboard[row][col] = 0
            else:
                children = tree.children(previous)
                previous = children[random.randint(0, len(children)-1)]
                gameboard[row][col] = previous.get_element()
                col += 1
    solution = copy.deepcopy(gameboard)
    for row in range(9):
        for col in range(9):
            if random.random() <= 0.64:
                gameboard[row][col] = 0
                empty_spaces += 1
    return solution, gameboard, empty_spaces


def save_game():
    data = json.load(open(PATH + "\\data.json"))
    data["og_gameboard"] = og_gameboard
    data["gameboard"] = gameboard
    data["time"] = pg.time.get_ticks()
    # change difficulty
    data["difficulty"] = 1
    outfile = open("data.json", "w")
    json.dump(data, outfile)
    outfile.close()


def load_game():
    data = json.load(open(PATH + "\\data.json"))
    return data["og_gameboard"], data["gameboard"], data["time"]


def draw_gameboard():
    """
    Draws the gameboard on the game window
    """
    pos = (int((WIDTH - size)/2), 25)
    gameboard_rect = pg.Rect(pos[0], pos[1], size, size)
    # draws lines
    for i in range(size//9, size-9, size//9):
        if i % 3 == 0:
            line_thickness = 2
        else:
            line_thickness = 1
        pg.draw.line(WINDOW, DARK_GRAY, (pos[0]+i, pos[1]), (pos[0]+i,
                     pos[1]+size), line_thickness)
        pg.draw.line(WINDOW, DARK_GRAY, (pos[0], pos[1]+i), (pos[0]+size,
                     pos[1]+i), line_thickness)
    # draws box
    pg.draw.rect(WINDOW, BLACK, gameboard_rect, 3)
    # draws numbers
    for row in range(9):
        for col in range(9):
            if og_gameboard[row][col] != 0:
                font = pg.font.SysFont('segoeuisemibold', 36)
            else:
                font = pg.font.SysFont('segoeui', 36)
            if gameboard[row][col] != 0:
                num = font.render(str(gameboard[row][col]), True, BLACK)
                WINDOW.blit(num, ((col*50)+pos[0]+16, (row*50)+pos[1]-2))
    return gameboard_rect


def draw_button(x, y, width, height, color, text="", font_size=25):
    """
    A general function used to draw a button, returns the buttons rect object
    """
    button = pg.Rect(x, y, width, height)
    pg.draw.rect(WINDOW, (color[0]-50, color[1]-50, color[2]-50), button)
    pg.draw.rect(WINDOW, color, (x+2, y+2, width-4, height-4))
    text = pg.font.SysFont('ebrima', 25).render(text, True, BLACK)
    text_pos = (x + (width//2) - (text.get_rect().width//2),
                y + (height//2) - (text.get_rect().height//2))
    WINDOW.blit(text, text_pos)
    return button


def draw_title_screen():
    """
    draws the title menu
    """
    WINDOW.fill(WHITE)
    text = pg.font.SysFont('ebrima', 70).render('Sudoku', True, BLACK)
    textRect = text.get_rect()
    WINDOW.blit(text, (WIDTH//2 - textRect.width//2, HEIGHT//2 -
                ((textRect.height//2) + 180)))


def show_time():
    """
    displays the time as text on the game window
    """
    time = (timer//1000)
    time_text = str(100 + time // 60)[1:3] + ":" + str(100 + time % 60)[1:3]
    text = pg.font.SysFont('ebrima', 25).render(time_text+str(), True, BLACK)
    WINDOW.blit(text, ((WIDTH//2)-28, 625))


og_gameboard = None
gameboard = None
running = True
game_running = False
empty_spaces = 0
timer = 0
solution = []
draw_title_screen()
start_button = draw_button((WIDTH//2)-75, 300, 160, 60, LIGHT_GRAY, "start", 24)
load_button = draw_button((WIDTH//2)-75, 400, 160, 60, LIGHT_GRAY,
                          "load save", 24)
# while loop for title menu
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONUP:
            mouse_pos = pg.mouse.get_pos()
            if start_button.collidepoint(mouse_pos) or game_running:
                try:
                    solution, og_gameboard, empty_spaces = create_solution()
                    gameboard = copy.deepcopy(og_gameboard)
                    running = False
                    game_running = True
                except AttributeError:
                    game_running = True
            elif load_button.collidepoint(mouse_pos):
                running = False
                game_running = True
                og_gameboard, gameboard, timer = load_game()
    pg.display.update()
# initialize mouse position
col = 0
row = 0
errors = []
notes = []
won = False
CLOCK.tick(30)
# second while loop for actual gameplay
while game_running:
    WINDOW.fill(WHITE)
    for pos in errors:
        pg.draw.rect(WINDOW, YELLOW, (50*pos[0]+137, 50*pos[1]+25, 50, 50))
    if won:
        rect = (int((WIDTH - size)/2), 25, size, size)
        pg.draw.rect(WINDOW, (150, 255, 150), rect)
        text = pg.font.SysFont('ebrima', 25).render("You Won!", True, BLACK)
        WINDOW.blit(text, ((WIDTH//2)-45, 485))
    else:
        timer += CLOCK.tick(30)
    gameboard_rect = draw_gameboard()
    # buttons
    save_game_button = draw_button(215, 535, 145, 45, LIGHT_GRAY, "save game")
    clear_button = draw_button(380, 535, 120, 45, LIGHT_GRAY, "clear")
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = pg.mouse.get_pos()
            if gameboard_rect.collidepoint(mouse_pos):
                col = (mouse_pos[0]-137)//50
                row = (mouse_pos[1]-25)//50
            elif save_game_button.collidepoint(mouse_pos):
                save_game()
            elif clear_button.collidepoint(mouse_pos):
                gameboard = og_gameboard
                errors = []
        elif event.type == pg.KEYDOWN and og_gameboard[row][col] == 0:
            if event.key == pg.K_h:
                gameboard = solution
                empty_spaces = 0
            elif event.key == pg.K_BACKSPACE and gameboard[row][col] != 0:
                gameboard[row][col] = 0
                empty_spaces += 1
            else:
                try:
                    num = int(event.unicode)
                    if event.mod & pg.KMOD_LSHIFT:
                        notes.append((row, col, num))
                    else:
                        if gameboard[row][col] == 0:
                            empty_spaces -= 1
                        gameboard[row][col] = num
                except Exception:
                    pass
            errors = check_board(gameboard)
            if len(errors) == 0 and empty_spaces == 0:
                won = True
    # draws a red square around selected cell on the gameboard
    pg.draw.rect(WINDOW, RED, (50*col+137, 50*row+25, 50, 50), 3)
    show_time()
    pg.display.update()
pg.quit()

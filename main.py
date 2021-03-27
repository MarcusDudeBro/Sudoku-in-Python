"""
    Author: Marcus Casillas
    Version: 2.0.0
"""
from game import Game

g = Game()
while g.running:
    if not g.playing:
        g.menu_loop()
    g.game_loop()

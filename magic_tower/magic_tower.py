import pygame
from pygame.locals import QUIT
from pygame.locals import KEYDOWN, KEYUP

from lega.screen import scrmgr

from lega.misc import terminate

class GameController:
    def initialize_game(self):

        # If called from pygame_boy_advance.py,
        # the following steps are unnecessary.
        # However, if run as a standalone program, they are necessary.
        # Besides, calling them redundantly has little performance impact.
        pygame.init()
        scrmgr.clear_screen_without_update()

        # Starting from here, all remaining steps are necessary.

        pygame.display.set_caption("Magic Tower")

        self.game_running = True

    def start_game(self):
        while self.game_running:
            self.one_frame()
    
    def one_frame(self):
        for e in pygame.event.get():
            if e.type == QUIT:
                terminate()
            elif e.type == KEYUP:
                ...
        
        scrmgr.tick()

def main():
    game = GameController()
    game.initialize_game()
    game.start_game()

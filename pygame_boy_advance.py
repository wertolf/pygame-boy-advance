import pygame
from pygame.locals import QUIT
from pygame.locals import KEYUP

from lega.screen import scrmgr
from lega.calc import calculate_centery
import lega.draw

import card_prisoner
from magic_tower import magic_tower

from config import filenames, key_bindings

import logging
import os.path

from enum import Enum

BANNER = "Mini-Game Projects Demo"
WINDOW_CAPTION = "Pygame Boy Advance"

class Options(str, Enum):
    QUIT = "Quit"
    CARD_PRISONER = "Card Prisoner"
    MAGIC_TOWER = "Magic Tower"
    CHINESE_CHECKERS = "Chinese Checkers"
    SUDOKU = "Sudoku"

def draw_banner():
    """
    绘制横幅
    """
    centery = scrmgr.win_width // 16
    lega.draw.text_single_line(
        scrmgr.screen, BANNER,
        font_size=scrmgr.font_size_large,
        centerx=scrmgr.center.x, centery=centery,
    )

def draw_option_list(options, selected_index):
    """
    绘制选项列表
    """
    centery = calculate_centery(len(options), scrmgr.center.y, scrmgr.default_line_distance)
    for i, opt in enumerate(options):
        lega.draw.text_single_line(
            scrmgr.screen, opt,
            selected=(i == selected_index),
            centerx=scrmgr.center.x, centery=centery,
        )
        centery += scrmgr.default_line_distance

def draw_everything(options, selected_index):
    scrmgr.clear_screen_without_update()
    draw_banner()
    draw_option_list(options, selected_index)

    # 把 update_global 放进 draw_everything
    # 可以减少 while 循环里面的重复性的代码
    # 同时由于设计上的简化，我也不打算在 draw_everything 之外的函数中调用 update_global
    scrmgr.update_global()

def main():
    # initialization
    pygame.init()
    pygame.display.set_caption(WINDOW_CAPTION)
    if not os.path.exists(filenames.PROGRAM_DATA_DIR):
        # create directory as needed
        os.mkdir(filenames.PROGRAM_DATA_DIR)
    options = [
        Options.CARD_PRISONER,
        Options.MAGIC_TOWER,
        # Options.CHINESE_CHECKERS,
        # Options.SUDOKU,
        Options.QUIT,
    ]
    selected_index = 0

    draw_everything(options, selected_index)

    while True:
        for e in pygame.event.get():
            if e.type == QUIT:
                return
            elif e.type == KEYUP:
                key = getattr(e, "key")
                if key == key_bindings.CONFIRM:
                    match options[selected_index]:
                        case Options.QUIT:
                            return
                        case Options.CARD_PRISONER:
                            card_prisoner.main()
                        case Options.MAGIC_TOWER:
                            magic_tower.main()

                    # when return from one of the games, redraw everything
                    pygame.display.set_caption(WINDOW_CAPTION)
                    draw_everything(options, selected_index)
                elif key == key_bindings.DOWN:
                    if selected_index < len(options) - 1:
                        selected_index += 1
                        draw_everything(options, selected_index)
                elif key == key_bindings.UP:
                    if selected_index > 0:
                        selected_index -= 1
                        draw_everything(options, selected_index)
        
        scrmgr.tick()

if __name__ == "__main__":
    main()
    pygame.quit()

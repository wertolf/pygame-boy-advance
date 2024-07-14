import pygame
from pygame.locals import QUIT
from pygame.locals import KEYUP

from lega.screen import scrmgr
from lega.calc import calculate_centery
import lega.draw

import card_prisoner.main
import magic_tower.main

from config import key_binding

import logging

from enum import Enum

BANNER = "Mini-Game Projects Demo"
WINDOW_CAPTION = "Pygame Boy Advance"

class Options(str, Enum):
    QUIT = "Quit"
    CARD_PRISONER = "Card Prisoner"
    MAGIC_TOWER = "Magic Tower"
    CHINESE_CHECKERS = "Chinese Checkers"

def draw_banner():
    """
    绘制横幅
    """
    font_size = scrmgr.win_width // 16 // 2
    centery = scrmgr.win_width // 16
    lega.draw.text_single_line(
        scrmgr.screen, BANNER,
        size=font_size,
        centerx=scrmgr.center.x, centery=centery,
    )

def draw_option_list(options, selected_index):
    """
    绘制选项列表
    """
    line_distance = scrmgr.win_width // 16 // 2
    centery = calculate_centery(len(options), scrmgr.center.y, line_distance)
    for i, opt in enumerate(options):
        lega.draw.text_single_line(
            scrmgr.screen, opt,
            selected=(i == selected_index),
            centerx=scrmgr.center.x, centery=centery,
        )
        centery += line_distance

def draw_everything(options, selected_index):
    scrmgr.clear_screen_without_update()
    draw_banner()
    draw_option_list(options, selected_index)

def main():
    # initialization
    pygame.init()
    pygame.display.set_caption(WINDOW_CAPTION)
    options = [
        Options.CARD_PRISONER,
        Options.MAGIC_TOWER,
        # Options.CHINESE_CHECKERS,
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
                if key == key_binding.confirm:
                    match options[selected_index]:
                        case Options.QUIT:
                            return
                        case Options.CARD_PRISONER:
                            card_prisoner.main.main()
                        case Options.MAGIC_TOWER:
                            magic_tower.main.main()

                    # when return from one of the games, redraw everything
                    pygame.display.set_caption(WINDOW_CAPTION)
                    draw_everything(options, selected_index)
                elif key == key_binding.down:
                    if selected_index < len(options) - 1:
                        selected_index += 1
                        draw_everything(options, selected_index)
                elif key == key_binding.up:
                    if selected_index > 0:
                        selected_index -= 1
                        draw_everything(options, selected_index)
        
        scrmgr.update_global()

if __name__ == "__main__":
    main()
    pygame.quit()

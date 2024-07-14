import pygame
from pygame.locals import QUIT
from pygame.locals import KEYUP

from lega.screen import scrmgr
from lega.calc import calculate_centery
from lega.draw import text_single_line

import card_prisoner.main

from config import key_binding

import logging

def draw_banner():
    """
    绘制横幅
    """
    banner = "Mini-Game Projects Demo"

    centery = 80  # scrmgr.win_height / 9
    text_single_line(
        scrmgr.screen, banner,
        size=40,
        centerx=scrmgr.center.x, centery=centery,
    )

def draw_option_list(options, selected_index):
    """
    绘制选项列表
    """
    line_distance = 40
    centery = calculate_centery(len(options), scrmgr.center.y, line_distance)
    for i, opt in enumerate(options):
        text_single_line(
            scrmgr.screen, opt,
            selected=(i == selected_index),
            centerx=scrmgr.center.x, centery=centery,
        )
        centery += line_distance

def main():
    # initialization
    pygame.init()
    pygame.display.set_caption("Pygame Boy Advance")
    options = [
        "Card Prisoner",
        # "Chinese Checkers",
        # "Magic Tower",
        "Quit",
    ]
    selected_index = 0
    draw_banner()
    draw_option_list(options, selected_index)

    while True:
        for e in pygame.event.get():
            if e.type == QUIT:
                return
            elif e.type == KEYUP:
                key = getattr(e, "key")
                if key == key_binding.confirm:
                    opt = options[selected_index]
                    if opt == "Quit":
                        return
                    elif opt == "Card Prisoner":
                        card_prisoner.main.main()
                        # redraw everything
                        pygame.display.set_caption("Pygame Boy Advance")
                        scrmgr.clear_screen_without_update()
                        draw_banner()
                        draw_option_list(options, selected_index)
                    else:
                        print(f"Oops! The game {opt} does not yet exist!")
                        logging.critical(f"Got unsupported option: {opt}")
                elif key == key_binding.down:
                    if selected_index < len(options) - 1:
                        selected_index += 1
                        scrmgr.clear_screen_without_update()
                        draw_banner()
                        draw_option_list(options, selected_index)
                elif key == key_binding.up:
                    if selected_index > 0:
                        selected_index -= 1
                        scrmgr.clear_screen_without_update()
                        draw_banner()
                        draw_option_list(options, selected_index)
        
        scrmgr.update_global()

if __name__ == "__main__":
    main()
    pygame.quit()

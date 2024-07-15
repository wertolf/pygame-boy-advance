import sys

import pygame_boy_advance
import magic_tower.static_preview

import logging

if __name__ == "__main__":
    if len(sys.argv) == 1:
        pygame_boy_advance.main()
    else:
        match sys.argv[1]:
            case "magic_tower_static":
                magic_tower.static_preview.main()
            case _:
                logging.critical(f"Got unknown argument: {sys.argv[1]}")


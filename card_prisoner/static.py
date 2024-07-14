"""
静态界面

用于早期界面布局规划
"""
import pygame
from pygame.locals import *
from pygame import Color
from pygame import Rect
from pygame import Surface
from collections import namedtuple
import math
import pygame.font

from lega.draw import text_single_line
from lega.calc import calculate_centery

WIN_WIDTH = 1280
WIN_HEIGHT = 720
BORDER_THICKNESS = 2
BORDER_RADIUS = 20  # 圆角矩形相关

WHITE = Color(255, 255, 255)
YELLOW = Color(255, 255, 0)
DARK_YELLOW = Color(128, 128, 0)

screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

Point = namedtuple("Point", ["x", "y"])
Vector2D = namedtuple("Vector2D", ["x", "y"])

clock = pygame.time.Clock()
fps = 10

def draw_status_bar():
    bar_width = 320  # 1280 / 4
    bar_height = 720
    bar_surface = Surface((bar_width, bar_height))
    bar_rect = Rect(0, 0, bar_width, bar_height)
    padding_x = 80
    padding_y = 40
    border_rect = Rect(
        padding_x * 0.5, padding_y * 0.5,
        bar_width - padding_x, bar_height - padding_y,
    )

    pygame.draw.rect(bar_surface, WHITE, border_rect, BORDER_THICKNESS, BORDER_RADIUS)

    distance = 40

    # upper half

    day = 1
    money = 80
    status = "Normal"
    hunger = 55
    thirst = 30
    sanity = 20
    labels = [  # top-down
        f"Day {day:02d}",
        f" Money: {money:7d}",
        f"Status: {status:>7}",
        f"Hunger: {hunger:3d}/100",
        f"Thirst: {thirst:3d}/100",
        f"Sanity: {sanity:3d}/100",
    ]

    """
    Simplicity favors regularity.
    """

    centery = border_rect.top
    for label in labels:
        centery += distance
        text_single_line(
            bar_surface, label,
            centerx=border_rect.centerx,
            centery=centery,
        )

    # lower half

    labels = [  # bottom-up
        "Back",
        "End Today",
        "Skills",
        "Inventory",
        "Shop",
    ]

    centery = border_rect.bottom
    for label in labels:
        centery -= distance
        text_single_line(
            bar_surface, label,
            centerx=border_rect.centerx,
            centery=centery,
        )

    # bullet (indicating current selection)

    i = 3
    radius = 5
    center = (
        border_rect.left + 40,
        border_rect.bottom - i * distance,
    )
    pygame.draw.circle(bar_surface, WHITE, center, radius)
    center = (
        border_rect.right - 40,
        border_rect.bottom - i * distance,
    )
    pygame.draw.circle(bar_surface, WHITE, center, radius)

    screen.blit(bar_surface, bar_rect)

def draw_card(target_surface, text, selected=False, **kwargs):
    """
    Specify position using kwargs.
    """
    card_width = 80
    card_height = 80
    card_surface = Surface((card_width, card_height))
    card_rect = Rect(0, 0, card_width, card_height)

    if selected:
        pygame.draw.rect(
            card_surface,
            YELLOW,
            card_rect,
            BORDER_THICKNESS * 2,
            BORDER_RADIUS,
        )
    else:
        pygame.draw.rect(
            card_surface,
            WHITE,
            card_rect,
            BORDER_THICKNESS,
            BORDER_RADIUS
        )

    centery = card_rect.centery - 20
    lines = text.split("\n")
    for line in lines:
        text_single_line(
            card_surface, line,
            centerx=card_rect.centerx,
            centery=centery,
        )
        centery += 20

    card_rect = card_surface.get_rect(**kwargs)

    target_surface.blit(card_surface, card_rect)


def draw_inventory():
    total_width = 960  # 1280 * 3/4
    total_height = 400  # 720 * 5/9
    local_surface = Surface((total_width, total_height))
    local_rect = local_surface.get_rect(bottom=WIN_HEIGHT, right=WIN_WIDTH)
    padding_x = 80
    padding_top = 10
    padding_bottom = 20
    padding_y = padding_top + padding_bottom
    border_width = total_width - padding_x
    border_height = total_height - padding_y
    border_rect = Rect(
        padding_x * 0.5, padding_top,
        border_width, border_height,
    )

    pygame.draw.rect(local_surface, WHITE, border_rect, BORDER_THICKNESS, BORDER_RADIUS)

    distance_x = 40 + 40 + 40 # 我的 40 你的 40 还有我们中间的 40
    distance_y = 40 + 20 + 40 # 我的 40 你的 40 还有我们中间的 20

    centerx_base = border_rect.left + 40 + 40
    centery_base = border_rect.top + 40 + 40 + 5
    # 之所以额外加 5 是因为后来缩小了 inventory 和 textbox 之间的空隙

    labels = [
        [
            "\nSSR\n0",
            "\nSR\n1",
            "\nR\n5",
            "\nA\n15",
            "\nB\n50",
            "\nC\n80",
            "\n\n",
        ],
        [
            "\nFood\n2",
            "\nWater\n3",
            "\n\n",
            "\n\n",
            "\n\n",
            "\n\n",
            "\n\n",
        ],
        [
            "\n???\n1",
            "\n???\n1",
            "\n\n",
            "\n\n",
            "\n\n",
            "\n\n",
            "\n\n",
        ]
    ]

    # row 1

    centerx = centerx_base
    centery = centery_base

    for card_info in labels[0]:
        draw_card(local_surface, card_info, centerx=centerx, centery=centery)
        centerx += distance_x
    
    # row 2

    centerx = centerx_base
    centery += distance_y

    for card_info in labels[1]:
        draw_card(local_surface, card_info, centerx=centerx, centery=centery)
        centerx += distance_x

    # row 3

    centerx = centerx_base
    centery += distance_y

    for card_info in labels[2]:
        draw_card(local_surface, card_info, centerx=centerx, centery=centery)
        centerx += distance_x
    
    # selecting effect

    i = 1
    j = 1
    centerx = centerx_base + distance_x * j
    centery = centery_base + distance_y * i

    draw_card(local_surface, labels[i][j], selected=True, centerx=centerx, centery=centery)
    
    screen.blit(local_surface, local_rect)

def draw_textbox(text):
    total_width = 960  # 1280 * 3/4
    total_height = 320  # 720 * 4/9
    local_surface = Surface((total_width, total_height))
    local_rect = local_surface.get_rect(top=0, right=WIN_WIDTH)
    padding_x = 80
    padding_top = 20
    padding_bottom = 10
    padding_y = padding_top + padding_bottom
    border_width = total_width - padding_x
    border_height = total_height - padding_y
    border_rect = Rect(
        # left and top are relative to local surface
        padding_x * 0.5, padding_top,
        border_width, border_height,
    )

    pygame.draw.rect(local_surface, WHITE, border_rect, BORDER_THICKNESS, BORDER_RADIUS)

    lines = text.split("\n")

    n_lines = len(lines)
    distance = 40
    centery = calculate_centery(n_lines, border_rect.centery, distance)

    for line in lines:
        text_single_line(local_surface, line, centerx=border_rect.centerx, centery=centery)
        centery += distance

    screen.blit(local_surface, local_rect)

def main():
    # init
    pygame.init()
    draw_status_bar()
    draw_inventory()
    draw_textbox("This card gives you some water.\nEffect: Thirst += 20.")
    game_running = True
    while game_running:
        for e in pygame.event.get():
            if e.type == QUIT:
                game_running = False
                break
        
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()


if __name__ == "__main__":
    main()

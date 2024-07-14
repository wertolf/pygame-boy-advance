from config import color_theme
from lega.screen import scrmgr
from lega.draw import text_single_line


import pygame
from pygame import Rect, Surface

from enum import Enum

class SideBarOptions(Enum):
    BACK = "Back"
    END_TODAY = "End Today"
    INVENTORY = "Inventory"
    SHOP = "Shop"
    SKILLS = "Skills"
    ABOUT = "About"


class SideBar:

    options = [  # bottom-up
        SideBarOptions.BACK,
        SideBarOptions.END_TODAY,
        SideBarOptions.INVENTORY,
        SideBarOptions.SHOP,
        SideBarOptions.SKILLS,
        SideBarOptions.ABOUT,
    ]

    def __init__(self):
        self.width = scrmgr.win_width / 4
        self.height = scrmgr.win_height
        self.surface = Surface((self.width, self.height))
        self.rect = Rect(0, 0, self.width, self.height)
        self.padding_x = scrmgr.win_width / 16
        self.padding_y = scrmgr.win_height / 9 / 2
        self.border_rect = Rect(
            self.padding_x * 0.5, self.padding_y * 0.5,
            self.width - self.padding_x, self.height - self.padding_y,
        )
        self.border_thickness = int(scrmgr.win_width / 16 / 40)
        self.border_radius = int(scrmgr.win_width / 16 / 4)
        self.line_distance = scrmgr.win_width / 16 / 2

        self.is_activated = False

    def draw_everything(self, player, selected_index):
        self.surface.fill(color_theme.background)
        self.draw_border()
        self.draw_upper(player)
        self.draw_lower(selected_index)
        scrmgr.screen.blit(self.surface, self.rect)

    def draw_border(self):
        if self.is_activated:
            pygame.draw.rect(self.surface, color_theme.foreground, self.border_rect, self.border_thickness, self.border_radius)
        else:
            pygame.draw.rect(self.surface, color_theme.disabled, self.border_rect, self.border_thickness, self.border_radius)

    def draw_upper(self, player):
        """
        Simplicity favors regularity.
        """
        labels = [  # top-down
            f"Day {player.age:02d}",
            f" Money: {player.money:7d}",
            f"Status: {player.status.value:>7}",
            f"Health: {player.health:3d}/100",
            f"Thirst: {player.thirst:3d}/100",
            f"Sanity: {player.sanity:3d}/100",
        ]

        line_distance = 40
        centery = self.border_rect.top
        for label in labels:
            centery += line_distance
            text_single_line(
                self.surface, label,
                centerx=self.border_rect.centerx,
                centery=centery,
            )

    def draw_lower(self, selected_index):
        centery = self.border_rect.bottom
        for i, option in enumerate(self.options):
            centery -= self.line_distance
            selected = (i == selected_index)
            if self.is_activated:
                color = color_theme.foreground
            else:
                color = color_theme.disabled
                """
                we can also set "selected" to False here
                if that looks better
                """
            text_single_line(
                self.surface, option.value,
                color=color, selected=selected,
                centerx=self.border_rect.centerx,
                centery=centery,
            )

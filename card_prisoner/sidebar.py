from config import color_theme
from lega.screen import scrmgr
import lega.draw

import pygame
from pygame import Rect, Surface

from enum import Enum

class SideBarOptions(Enum):
    END_TODAY = "End Today"
    INVENTORY = "Inventory"
    SHOP = "Shop"
    SKILLS = "Skills"
    ABOUT = "About"


class SideBar:

    options = [  # bottom-up
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

        padding_x = scrmgr.win_width / 16
        padding_y = scrmgr.win_height / 9 / 2
        self.border_rect = Rect(
            padding_x * 0.5, padding_y * 0.5,
            self.width - padding_x, self.height - padding_y,
        )

        self.is_activated = False

    def draw_everything(self, player, selected_index):
        self.surface.fill(color_theme.background)
        self._draw_border()
        self._draw_upper(player)
        self._draw_lower(selected_index)

        scrmgr.screen.blit(self.surface, self.rect)
        scrmgr.update_local_area(self.rect)

    def _draw_border(self):
        if self.is_activated:
            color = color_theme.foreground
        else:
            color = color_theme.disabled

        pygame.draw.rect(
            self.surface,
            color,
            self.border_rect,
            scrmgr.default_border_thickness,
            scrmgr.default_border_radius,
        )

    def _draw_upper(self, player):
        """
        Simplicity favors regularity.
        """
        labels = [  # top-down
            f"Day {player.age}",
            f"$ {player.money}",
            f"HP: {player.HP:3d}/100",
            f"MP: {player.MP:3d}/100",
        ]

        centery = self.border_rect.top
        for label in labels:
            centery += scrmgr.default_line_distance
            lega.draw.text_single_line(
                self.surface, label,
                left=self.border_rect.left,
                centerx=self.border_rect.centerx,
                centery=centery,
            )

    def _draw_lower(self, selected_index):
        centery = self.border_rect.bottom
        for i, option in enumerate(self.options):
            centery -= scrmgr.default_line_distance
            selected = (i == selected_index)
            if self.is_activated:
                color = color_theme.foreground
            else:
                color = color_theme.disabled
                """
                we can also set "selected" to False here
                if that looks better
                """
            lega.draw.text_single_line(
                self.surface, option.value,
                color=color, selected=selected,
                centerx=self.border_rect.centerx,
                centery=centery,
            )

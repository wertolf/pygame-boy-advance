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
    TALENT = "Talent"
    ABOUT = "About"


class SideBar:

    options = [  # bottom-up
        SideBarOptions.END_TODAY,
        SideBarOptions.INVENTORY,
        SideBarOptions.SHOP,
        SideBarOptions.TALENT,
        SideBarOptions.ABOUT,
    ]

    def __init__(self):
        width = scrmgr.win_width / 4
        height = scrmgr.win_height
        self.surface = Surface((width, height))
        self.rect = Rect(0, 0, width, height)

        padding_x = scrmgr.win_width / 16
        padding_y = scrmgr.win_height / 9 / 2
        self.border_rect = Rect(
            padding_x * 0.5, padding_y * 0.5,
            width - padding_x, height - padding_y,
        )

        self.is_activated = False

        self.day = -1
        self.money_value = -1
        self.HP_value = -1
        self.MP_value = -1

        # 初始状态下，选择最上面的选项
        self._selected_option_index = len(self.options) - 1
    
    @property
    def selected_option_index(self):
        return self._selected_option_index
    
    @selected_option_index.setter
    def selected_option_index(self, value):
        if value < 0 or value > len(self.options) - 1:  # 合法性检查
            return

        self._selected_option_index = value

    def draw_everything(self):
        self.surface.fill(color_theme.background)
        self._draw_border()
        self._draw_upper()
        self._draw_lower()

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

    def _draw_upper(self):
        """
        Simplicity favors regularity.
        """
        labels = [  # top-down
            f"Day {self.day}",
            f"$ {self.money_value}",
            f"HP: {self.HP_value:3d}/100",
            f"MP: {self.MP_value:3d}/100",
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

    def _draw_lower(self):
        centery = self.border_rect.bottom
        for i, option in enumerate(self.options):
            centery -= scrmgr.default_line_distance
            selected = (i == self.selected_option_index)
            if self.is_activated:
                color = color_theme.foreground
            else:
                color = color_theme.disabled
                """
                we can also set "selected" to False here
                if that looks better
                """
            lega.draw.text_single_line(
                self.surface,
                option.value,
                color=color,
                selected=selected,
                centerx=self.border_rect.centerx,
                centery=centery,
            )

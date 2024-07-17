from lega.screen import scrmgr
import lega.draw

import logging

from pygame import Surface, Rect
import pygame.draw

from config import color_theme

from card_prisoner.item import (
    SSR,
    A,
    B,
    C,
    FOOD,
    WATER,
)
from card_prisoner.item import Item

from enum import Enum, IntEnum

class ItemListMode(Enum):
    EMPTY = 0
    INVENTORY = 1
    SHOP = 2
    TALENT = 3

class InventoryItemIndex(IntEnum):
    SSR = 0

    A = 3
    B = 4
    C = 5

    FOOD = 7
    WATER = 8

class ShopItemIndex(IntEnum):
    ON_SALE_ITEM_1 = 0
    WANTED_ITEM_1 = 14

class ItemList:
    items: list[Item]
    def __init__(self):
        width = scrmgr.win_width * 3 / 4
        height = scrmgr.win_height * 5 / 9
        self.surface = Surface((width, height))
        self.rect = self.surface.get_rect(bottom=scrmgr.win_height, right=scrmgr.win_width)

        padding_x = 80
        padding_top = 10
        padding_bottom = 20
        padding_y = padding_top + padding_bottom
        border_width = width - padding_x
        border_height = height - padding_y
        self.border_rect = Rect(
            padding_x * 0.5, padding_top,
            border_width, border_height,
        )

        # maximum: 3 rows, 7 columns
        self.n_rows = 3
        self.n_cols = 7

        self.mode = ItemListMode.EMPTY

        self.is_activated = False
        # 初始状态下，看不到被选中的 item
        # 每次进入 ItemList 的时候，将 index 置为 0
        self._selected_item_index = -1

    @property
    def selected_item_index(self):
        return self._selected_item_index
    
    @selected_item_index.setter
    def selected_item_index(self, value):
        if value < 0 or value > self.n_cols * self.n_rows - 1:  # 合法性检查
            return

        self._selected_item_index = value

    @property
    def color(self):
        if not self.is_activated:
            return color_theme.disabled
        else:
            return color_theme.foreground

    def _draw_border(self):
        pygame.draw.rect(
            self.surface,
            self.color,
            self.border_rect,
            scrmgr.default_border_thickness,
            scrmgr.default_border_radius,
        )

    def draw_everything(self):

        self.surface.fill(color_theme.background)
        self._draw_border()
        self._draw_items()

        scrmgr.screen.blit(self.surface, self.rect)
        scrmgr.update_local_area(self.rect)

    def _draw_items(self):
        distance_x = 40 + 40 + 40 # 我的 40 你的 40 还有我们中间的 40
        distance_y = 40 + 20 + 40 # 我的 40 你的 40 还有我们中间的 20

        centerx_base = self.border_rect.left + 40 + 40
        centery_base = self.border_rect.top + 40 + 40 + 5
        # 之所以额外加 5 是因为后来缩小了 inventory 和 textbox 之间的空隙

        # TODO: do not use hard-coded number of rows
        # TODO: duplicate code for 3 rows

        # row 1

        centerx = centerx_base
        centery = centery_base

        row = 0
        row_items = self.items[self.n_cols * row : self.n_cols * (row + 1)]
        for item in row_items:
            self._draw_item(self.surface, item, centerx=centerx, centery=centery)
            centerx += distance_x
        
        # row 2

        centerx = centerx_base
        centery += distance_y

        row = 1
        row_items = self.items[self.n_cols * row : self.n_cols * (row + 1)]
        for item in row_items:
            self._draw_item(self.surface, item, centerx=centerx, centery=centery)
            centerx += distance_x

        # row 3

        centerx = centerx_base
        centery += distance_y

        row = 2
        row_items = self.items[self.n_cols * row : self.n_cols * (row + 1)]
        for item in row_items:
            self._draw_item(self.surface, item, centerx=centerx, centery=centery)
            centerx += distance_x
        
        # selecting effect

        if self.is_activated:
            i = int(self.selected_item_index / self.n_cols)
            j = int(self.selected_item_index % self.n_cols)

            centerx = centerx_base + distance_x * j
            centery = centery_base + distance_y * i

            item = self.items[self.selected_item_index]
            self._draw_item(self.surface, item, selected=True, centerx=centerx, centery=centery)
        
    def _draw_item(self, target_surface: Surface, item: Item, selected=False, **kwargs):
        """
        Specify position using kwargs.
        """
        card_width = scrmgr.win_width // 16  # 80 under 1280x720
        card_height = card_width
        card_surface = Surface((card_width, card_height))
        card_rect = Rect(0, 0, card_width, card_height)

        border_thickness = scrmgr.default_border_thickness
        if selected:
            color = color_theme.selected
            border_thickness *= 2
        else:
            color = self.color

        pygame.draw.rect(
            card_surface,
            color,
            card_rect,
            border_thickness,
            scrmgr.default_border_radius,
        )

        lega.draw.text_multi_line(
            card_surface,
            str(item),  # 调用 item.__str__()
            reference_point=(card_rect.centerx, card_rect.centery),

            line_distance=(scrmgr.default_line_distance // 2),
            color=color,
        )

        card_rect = card_surface.get_rect(**kwargs)

        target_surface.blit(card_surface, card_rect)

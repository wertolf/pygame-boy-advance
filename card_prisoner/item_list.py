from lega.draw import text_single_line
from lega.screen import scrmgr

import logging

from pygame import Surface, Rect
import pygame.draw

from config import color_theme

from card_prisoner.constants import BORDER_RADIUS

from card_prisoner.constants import BORDER_THICKNESS
from card_prisoner.item import Item
from card_prisoner.card import CardNames

from enum import Enum, IntEnum

class ItemListMode(Enum):
    EMPTY = 0
    INVENTORY = 1
    SHOP = 2
    SKILLS = 3

class InventoryItemIndex(IntEnum):
    SSR = 0
    SR = 1
    R = 2
    A = 3
    B = 4
    C = 5
    FOOD = 7
    WATER = 8
    ASPIRIN = 10
    VITAMIN = 11
    TRANQUILIER = 12

class ShopItemIndex(IntEnum):
    DRAW_1_CARD = 14
    DRAW_5_CARDS = 15
    DRAW_10_CARDS = 16

class SkillItemIndex(IntEnum):
    TALENT_1 = 0
    TALENT_2 = 1
    HUNGER_RESISTANCE = 7
    THIRST_RESISTANCE = 8

class ItemList:
    def __init__(self):
        self.width = scrmgr.win_width * 3 / 4
        self.height = scrmgr.win_height * 5 / 9
        self.surface = Surface((self.width, self.height))
        self.rect = self.surface.get_rect(bottom=scrmgr.win_height, right=scrmgr.win_width)

        padding_x = 80
        padding_top = 10
        padding_bottom = 20
        padding_y = padding_top + padding_bottom
        border_width = self.width - padding_x
        border_height = self.height - padding_y
        self.border_rect = Rect(
            padding_x * 0.5, padding_top,
            border_width, border_height,
        )

        # maximum: 3 rows, 7 columns
        self.n_rows = 3
        self.n_cols = 7

        self.is_activated = False

        self.mode = ItemListMode.EMPTY

    @property
    def color(self):
        if not self.is_activated:
            return color_theme.disabled
        else:
            return color_theme.foreground

    def make_items(self, player):
        self.items = [Item("")] * self.n_cols * self.n_rows

        match self.mode:
            case ItemListMode.EMPTY:
                pass
            case ItemListMode.INVENTORY:
                self.items[InventoryItemIndex.SSR] = player.inventory[CardNames.SSR]
                self.items[InventoryItemIndex.A] = player.inventory[CardNames.A]
                self.items[InventoryItemIndex.B] = player.inventory[CardNames.B]
                self.items[InventoryItemIndex.C] = player.inventory[CardNames.C]
                self.items[InventoryItemIndex.FOOD] = player.inventory[CardNames.FOOD]
                self.items[InventoryItemIndex.WATER] = player.inventory[CardNames.WATER]
                self.items[InventoryItemIndex.ASPIRIN] = player.inventory[CardNames.ASPIRIN]
            case ItemListMode.SHOP:
                ...
            case ItemListMode.SKILLS:
                self.items[SkillItemIndex.TALENT_1] = player.talents[0]
                self.items[SkillItemIndex.TALENT_2] = player.talents[1]

    def draw_border(self):
        pygame.draw.rect(self.surface, self.color, self.border_rect, BORDER_THICKNESS, BORDER_RADIUS)

    def draw_everything(self, player, selected_index):

        self.surface.fill(color_theme.background)

        self.draw_border()

        distance_x = 40 + 40 + 40 # 我的 40 你的 40 还有我们中间的 40
        distance_y = 40 + 20 + 40 # 我的 40 你的 40 还有我们中间的 20

        centerx_base = self.border_rect.left + 40 + 40
        centery_base = self.border_rect.top + 40 + 40 + 5
        # 之所以额外加 5 是因为后来缩小了 inventory 和 textbox 之间的空隙

        self.make_items(player)

        # TODO: do not use hard-coded number of rows
        # TODO: duplicate code for 3 rows

        # row 1

        centerx = centerx_base
        centery = centery_base

        row = 0
        row_items = self.items[self.n_cols * row : self.n_cols * (row + 1)]
        for item in row_items:
            item_text = str(item)
            draw_item(self.surface, item_text, color=self.color, centerx=centerx, centery=centery)
            centerx += distance_x
        
        # row 2

        centerx = centerx_base
        centery += distance_y

        row = 1
        row_items = self.items[self.n_cols * row : self.n_cols * (row + 1)]
        for item in row_items:
            item_text = str(item)
            draw_item(self.surface, item_text, color=self.color, centerx=centerx, centery=centery)
            centerx += distance_x

        # row 3

        centerx = centerx_base
        centery += distance_y

        row = 2
        row_items = self.items[self.n_cols * row : self.n_cols * (row + 1)]
        for item in row_items:
            item_text = str(item)
            draw_item(self.surface, item_text, color=self.color, centerx=centerx, centery=centery)
            centerx += distance_x
        
        # selecting effect

        if self.is_activated:
            i = int(selected_index / self.n_cols)
            j = int(selected_index % self.n_cols)

            centerx = centerx_base + distance_x * j
            centery = centery_base + distance_y * i

            item = self.items[selected_index]
            item_text = str(item)
            draw_item(self.surface, item_text, selected=True, color=self.color, centerx=centerx, centery=centery)
        
        scrmgr.screen.blit(self.surface, self.rect)
        scrmgr.update_local_area(self.rect)

def draw_item(target_surface, text, selected=False, **kwargs):
    """
    Specify position using kwargs.
    """
    color = kwargs.pop("color", color_theme.foreground)

    card_width = 80
    card_height = 80
    card_surface = Surface((card_width, card_height))
    card_rect = Rect(0, 0, card_width, card_height)

    border_thickess = BORDER_THICKNESS
    if selected:
        color = color_theme.selected
        border_thickess *= 2

    pygame.draw.rect(card_surface, color, card_rect, border_thickess, BORDER_RADIUS)

    centery = card_rect.centery - 20
    if text is None:
        lines = []
    else:
        lines = text.split("\n")
    for line in lines:
        text_single_line(
            card_surface, line,
            color=color,
            centerx=card_rect.centerx,
            centery=centery,
        )
        centery += 20

    card_rect = card_surface.get_rect(**kwargs)

    target_surface.blit(card_surface, card_rect)
import pygame
import pygame.draw
from pygame.locals import QUIT
from pygame.locals import KEYUP, KEYDOWN

from card_prisoner.card import SUPPLY, CardNames
from card_prisoner.constants import PRICE_PER_CARD
from card_prisoner.player import Player
from card_prisoner.view import View
from card_prisoner.view import ViewMode
from card_prisoner.item_list import InventoryItemIndex, ShopItemIndex, ItemListMode
from card_prisoner.sidebar import SideBarOptions
from card_prisoner import messages
from lega.screen import scrmgr
from card_prisoner.constants import KEYDOWN_INITIAL_INTERVAL, DRAW_CARD_TIME_INTERVAL

from lega.misc import terminate, display_help, take_screenshot
from lega.an import global_fadeout

import lega.draw

from config import filenames, key_bindings, color_theme

import time
import logging
import pickle
import os.path
import math
import random

WINDOW_CAPTION = "Card Prisoner"






class GameController:
    def initialize_game(self):
        """
        initialization
        """

        # if __name__ == "__main__" the following steps are redundant
        # but if called from another script they may be necessary
        pygame.init()
        scrmgr.clear_screen_without_update()
        scrmgr.update_global()

        # the following steps should all be necessary

        pygame.display.set_caption(WINDOW_CAPTION)

        self.player = Player()
        self.view = View()

        self.view.draw_everything(self.player)

        # following are main loop variables

        self.game_running = True
        self.pressed_key = None
        self.is_holding_key = False
        self.key_holding_timer = 0
        self.draw_card_timer = 0

    def start_game(self):

        while self.game_running:

            # timer-related logic

            if self.pressed_key is not None:
                # 若某个键处于被按下的状态

                if not self.is_holding_key:
                    # 若它还没有进入长按状态，则判断是否可以进入长按状态
                    time_elapsed = time.time() - self.key_holding_timer
                    if time_elapsed > KEYDOWN_INITIAL_INTERVAL:
                        self.is_holding_key = True
                else:
                    # 若已经进入长按状态，则重复执行该键对应的行为
                    match self.pressed_key:
                        case key_bindings.DRAW_CARD:
                            time_elapsed = time.time() - self.draw_card_timer
                            if time_elapsed > DRAW_CARD_TIME_INTERVAL:
                                # TODO: duplicate code in KEYDOWN handler
                                self._draw_card()

                                # TODO: duplicate code in KEYDOWN handler
                                if self.player.has_won():
                                    self.game_running = False
                                    break
                                    
                                self.draw_card_timer = time.time()
                        case _:
                            logging.critical(f"Got unsupported key holding: {self.pressed_key}")

            # event handling

            for e in pygame.event.get():
                if e.type == QUIT:
                    terminate()
                elif e.type == KEYDOWN:

                    # 用于识别长按
                    self.key_holding_timer = time.time()

                    key = getattr(e, "key")
                    match key:
                        case key_bindings.DRAW_CARD:
                            # 按下 D 键时立刻进行一次抽卡
                            # 如果持续按住 KEYDOWN_INITIAL_TIME_INTERVAL
                            # 则之后每隔 DRAW_CARD_TIME_INTERVAL 抽一次卡
                            self._draw_card()

                            # TODO: duplicate code (game over checking)
                            if self.player.has_won():
                                self.game_running = False
                                break
                                
                            self.pressed_key = key_bindings.DRAW_CARD
                            self.draw_card_timer = time.time()
                elif e.type == KEYUP:

                    # 重置用于识别长按的相关数据结构
                    self.is_holding_key = False
                    self.pressed_key = None

                    key = getattr(e, "key")
                    option = self.view.sidebar.options[self.view.sidebar_index]
                    if key == key_bindings.RETURN_TO_TITLE:
                        restart_game = False
                        return restart_game
                    elif key == key_bindings.PRINT_SCREEN:
                        take_screenshot()
                    elif key == key_bindings.CHEAT:
                        self._cheat()

                        # TODO: duplicate code (game over checking)
                        if self.player.has_won():
                            self.game_running = False
                            break
                    elif key == key_bindings.DRAW_CARD:
                        pass

                    elif key == key_bindings.CONFIRM:
                        match self.view.mode:
                            case ViewMode.LEVEL_1:
                                match option:
                                    case SideBarOptions.END_TODAY:
                                        self._end_today()

                                        if self.player.is_dead():
                                            self.game_running = False
                                            break
                                    case SideBarOptions.INVENTORY:
                                        self.view.mode = ViewMode.LEVEL_2
                                    case SideBarOptions.SHOP:
                                        self.view.mode = ViewMode.LEVEL_2
                                    case SideBarOptions.SKILLS:
                                        self.view.mode = ViewMode.LEVEL_2
                                    case _:
                                        logging.critical(f"Got unsupported action: {option}")
                            case ViewMode.LEVEL_2:
                                match self.view.item_list.mode:
                                    case ItemListMode.INVENTORY:
                                        match self.view.item_list_index:
                                            case InventoryItemIndex.FOOD:
                                                self._eat_food()
                                            case InventoryItemIndex.WATER:
                                                self._drink_water()
                                            case _:
                                                logging.critical(f"unsupported")
                                    case ItemListMode.SHOP:
                                        match self.view.item_list_index:
                                            case ShopItemIndex.DRAW_1_CARD:
                                                self._draw_card()
                                            case _:
                                                logging.critical(f"unsupported")
                            case _:
                                raise AssertionError(f"Got unexpected view mode: {self.view.mode}")
                    elif key == key_bindings.CANCEL:
                        if self.view.mode == ViewMode.LEVEL_2:
                            self.view.mode = ViewMode.LEVEL_1
                    elif key == key_bindings.UP:
                        if self.view.mode == ViewMode.LEVEL_1:
                            # 注意 actions 列表是自底向上的
                            # 所以 up 会增加索引值
                            # down 会减少索引值
                            self.view.sidebar_index += 1
                        elif self.view.mode == ViewMode.LEVEL_2:
                            self.view.item_list_index -= self.view.item_list.n_cols

                    elif key == key_bindings.DOWN:
                        if self.view.mode == ViewMode.LEVEL_1:
                            self.view.sidebar_index -= 1
                        elif self.view.mode == ViewMode.LEVEL_2:
                            self.view.item_list_index += self.view.item_list.n_cols
                    
                    elif key == key_bindings.LEFT:
                        if self.view.mode == ViewMode.LEVEL_2:
                            self.view.item_list_index -= 1

                    elif key == key_bindings.RIGHT:
                        if self.view.mode == ViewMode.LEVEL_2:
                            self.view.item_list_index += 1

                    elif key == key_bindings.SAVE_GAME:

                        # PROGRAM_DATA_DIR is created in pygame_boy_advance.py
                        assert os.path.exists(filenames.PROGRAM_DATA_DIR)

                        with open(filenames.CARD_PRISONER_SAVE_FILE, "wb") as file:
                            pickle.dump(player, file)
                        self.view.textbox.set_text(messages.SAVE_SUCCESS)

                    elif key == key_bindings.LOAD_GAME:
                        filename = filenames.CARD_PRISONER_SAVE_FILE
                        if os.path.exists(filename):
                            with open(filename, "rb") as file:
                                player = pickle.load(file)
                            self.view.textbox.set_text(messages.LOAD_SUCCESS)
                        else:
                            self.view.textbox.set_text(messages.LOAD_NOT_FOUND)
                    
                    elif key == key_bindings.DISPLAY_HELP:
                        display_help(messages.HELP)
                    else:
                        logging.critical(f"Ignored KEYUP: {key}")

            # 由于大多数事件都会修改 view 的某个局部
            # 所以出于简化的考虑，在循环末尾用一行代码可以省去在每一处都添加一行相同的代码
            # 唯一的影响是即使没有事件也会进行重绘
            # 但是这个问题可以在设定一个合适的 FPS 之后被后面的 tick 减轻
            self.view.draw_everything(self.player)

            scrmgr.tick()

        assert self.player.is_game_over()

        global_fadeout()  # 全局淡出
        if self.player.has_won():
            msg = (
                "Congratulations! You won!"
            )
        elif self.player.is_dead():
            msg = self.player.death_reason
        msg += (
            "\n"
            "\n"
            "(PRESS R TO RESTART)"
        )
        lega.draw.text_multi_line(
            scrmgr.screen,
            text=msg,
            reference_point=scrmgr.center,
            font_size=scrmgr.font_size_large,
            bold=False,
        )
        scrmgr.update_global()
        
        while True:
            for e in pygame.event.get():
                if e.type == QUIT:
                    terminate()
                elif e.type == KEYUP:
                    key = getattr(e, "key")
                    if key == key_bindings.RESTART_GAME:
                        restart_game = True
                        return restart_game
            
            scrmgr.tick()

    def _cheat(self):
        self.player.inventory[CardNames.FOOD].quantity += 5
        self.player.inventory[CardNames.WATER].quantity += 5

        self.view.textbox.set_text(
            "You pressed the cheat key.\n"
            "Got 5 food card.\n"
            "Got 5 water card."
        )

    def _draw_card(self):
        if self.player.money >= PRICE_PER_CARD:

            self.player.money -= PRICE_PER_CARD

            number = random.random()
            if number < 0.01:  # TODO: hard-coded value
                card = CardNames.SSR
            elif number < 0.05:
                card = CardNames.FOOD
            elif number < 0.1:
                card = CardNames.WATER
            elif number < 0.3:  # TODO: hard-coded value
                card = CardNames.A
            elif number < 0.6:  # TODO: hard-coded value
                card = CardNames.B
            else:
                card = CardNames.C

            self.player.inventory[card].quantity += 1

            text = "Got %s card." % card.name

            if card == CardNames.SSR:
                text = "GOT SSR CARD!!!"
            elif card not in SUPPLY:
                # TODO: decrease sanity by a random amount
                ...

            self.view.textbox.set_text(text)

        else:  # player.money < PRICE_PER_CARD
            self.view.textbox.set_text(
                "You do not have enough money!",
            )

    def _end_today(self):

        # update model

        self.player.sleep()

        # update view

        self.view.sidebar_index = self.view.sidebar_index  # call action_index.setter to update inventory properly

        msg = (
            f"*** Day {self.player.age:02d} ***\n"
            f"HP -= {self.player.HP_decrease_per_day}\n"
            f"MP -= {self.player.MP_decrease_per_day}\n"
        )

        self.view.textbox.set_text(msg)

    def _eat_food(self):
        # update model
        self.player.eat_food()

        # update view
        self.view.textbox.set_text("You ate some food.")

    def _drink_water(self):
        # update model
        self.player.drink_water()

        # update view
        self.view.textbox.set_text("You drank some water.")


def main():
    restart_game = True
    while restart_game:
        game = GameController()
        game.initialize_game()
        restart_game = game.start_game()


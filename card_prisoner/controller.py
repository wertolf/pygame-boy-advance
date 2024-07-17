import lega.draw
from card_prisoner import messages
from card_prisoner.card import SUPPLY, CardNames
from card_prisoner.constants import DRAW_CARD_TIME_INTERVAL, KEYDOWN_INITIAL_INTERVAL, PRICE_PER_CARD
from card_prisoner.item_list import InventoryItemIndex, ItemListMode, ShopItemIndex
from card_prisoner.player import Player
from card_prisoner.sidebar import SideBarOptions
from card_prisoner.view import View, ViewMode
from card_prisoner.talent import TALENT_DESC, TALENT_POOL
from config import filenames, key_bindings
from lega.an import global_fadeout
from lega.misc import display_help, take_screenshot, terminate
from lega.screen import scrmgr


import pygame
from pygame.locals import KEYDOWN, KEYUP, QUIT


import logging
import os.path
import pickle
import random
import time

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

        self._player = Player()
        self._view = View()

        self._view.draw_everything(self._player)

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

                            self.pressed_key = key_bindings.DRAW_CARD
                            self.draw_card_timer = time.time()
                elif e.type == KEYUP:

                    # 重置用于识别长按的相关数据结构
                    self.is_holding_key = False
                    self.pressed_key = None

                    key = getattr(e, "key")

                    if key == key_bindings.RETURN_TO_TITLE:
                        restart_game = False
                        return restart_game

                    elif key == key_bindings.PRINT_SCREEN:
                        take_screenshot()

                    elif key == key_bindings.CHEAT:
                        self._cheat()

                    elif key == key_bindings.DRAW_CARD:
                        pass
                
                    elif key in key_bindings.ARROW_KEYS:
                        self._on_arrow_key_up(key)

                    elif key == key_bindings.CONFIRM:
                        self._on_confirm()

                    elif key == key_bindings.CANCEL:
                        self._on_cancel()

                    elif key == key_bindings.SAVE_GAME:
                        self._on_save_game()

                    elif key == key_bindings.LOAD_GAME:
                        self._on_load_game()

                    elif key == key_bindings.DISPLAY_HELP:
                        display_help(messages.HELP)
                    else:
                        logging.critical(f"Ignored KEYUP: {key}")

            # 由于大多数事件都会修改 view 的某个局部
            # 所以出于简化的考虑，在循环末尾用一行代码可以省去在每一处都添加一行相同的代码
            # 唯一的影响是即使没有事件也会进行重绘
            # 但是这个问题可以在设定一个合适的 FPS 之后被后面的 tick 减轻
            self._view.draw_everything(self._player)

            scrmgr.tick()

        assert self._player.is_game_over()

        global_fadeout()  # 全局淡出
        if self._player.has_won():
            msg = (
                "Congratulations! You won!"
            )
        elif self._player.is_dead():
            msg = self._player.death_reason
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

    def _on_arrow_key_up(self, key):
        """
        为了减少 start_game 方法的行数而进行的封装
        类似于一个事件处理器，但是并不存在一个 ARROW_KEY_UP 的事件
        """
        match key:
            case key_bindings.UP:
                if self._view.mode == ViewMode.LEVEL_1:

                    # 注意 SideBar.options 列表是自底向上的
                    # 所以 up 会增加索引值
                    # down 会减少索引值
                    self._view.sidebar.selected_option_index += 1

                elif self._view.mode == ViewMode.LEVEL_2:
                    self._view.item_list.selected_item_index -= self._view.item_list.n_cols

            case key_bindings.DOWN:
                if self._view.mode == ViewMode.LEVEL_1:
                    self._view.sidebar.selected_option_index -= 1

                elif self._view.mode == ViewMode.LEVEL_2:
                    self._view.item_list.selected_item_index += self._view.item_list.n_cols
            
            case key_bindings.LEFT:
                if self._view.mode == ViewMode.LEVEL_2:
                    self._view.item_list.selected_item_index -= 1
            
            case key_bindings.RIGHT:
                if self._view.mode == ViewMode.LEVEL_2:
                    self._view.item_list.selected_item_index += 1
        
        self._update_default_message()

    def _on_confirm(self):
        """
        为了减少 start_game 方法的行数而进行的封装
        类似于一个事件处理器，但是并不存在一个 CONFIRM 事件
        """
        option = self._view.sidebar.options[self._view.sidebar.selected_option_index]
        match self._view.mode:
            case ViewMode.LEVEL_1:
                match option:
                    case SideBarOptions.END_TODAY:
                        self._end_today()

                    case SideBarOptions.INVENTORY:
                        # TODO: duplicate code
                        self._view.mode = ViewMode.LEVEL_2
                        self._view.item_list.mode = ItemListMode.INVENTORY
                        self._view.item_list.selected_item_index = 0
                        # self._view.item_list.make_items(self._player)
                    case SideBarOptions.SHOP:
                        ...
                    case SideBarOptions.SKILLS:
                        # TODO: duplicate code
                        self._view.mode = ViewMode.LEVEL_2
                        self._view.item_list.mode = ItemListMode.SKILLS
                        self._view.item_list.selected_item_index = 0
                        self._view.item_list.make_items(self._player)
                    case _:
                        logging.critical(f"Got unsupported action: {option}")
            case ViewMode.LEVEL_2:
                match self._view.item_list.mode:
                    case ItemListMode.INVENTORY:
                        match self._view.item_list.selected_item_index:
                            case InventoryItemIndex.FOOD:
                                self._eat_food()
                            case InventoryItemIndex.WATER:
                                self._drink_water()
                            case _:
                                logging.critical(f"unsupported")
                    case ItemListMode.SHOP:
                        match self._view.item_list.selected_item_index:
                            case ShopItemIndex.DRAW_1_CARD:
                                self._draw_card()
                            case _:
                                logging.critical(f"unsupported")
            case _:
                raise AssertionError(f"Got unexpected view mode: {self._view.mode}")

        self._update_default_message()

    def _on_cancel(self):
        """
        为了与 on_confirm 构成互补而进行的封装
        """
        if self._view.mode == ViewMode.LEVEL_2:
            self._view.mode = ViewMode.LEVEL_1
            self._view.item_list.mode = ItemListMode.EMPTY

        self._update_default_message()

    def _on_save_game(self):
        """
        为了提高 .start_game 方法的可读性而进行的封装
        类似于一个事件处理器，但是并不存在一个 SAVE_GAME 的事件
        也为后续实现更复杂的 存档 功能做准备
        """
        # PROGRAM_DATA_DIR is created in pygame_boy_advance.py
        assert os.path.exists(filenames.PROGRAM_DATA_DIR)

        with open(filenames.CARD_PRISONER_SAVE_FILE, "wb") as file:
            pickle.dump(self._player, file)
        self._view.textbox.set_text(messages.SAVE_SUCCESS)

    def _on_load_game(self):
        """
        为了提高 .start_game 方法的可读性而进行的封装
        类似于一个事件处理器，但是并不存在一个 LOAD_GAME 的事件
        也为后续实现更复杂的 读档 功能作准备
        """
        filename = filenames.CARD_PRISONER_SAVE_FILE
        if os.path.exists(filename):
            with open(filename, "rb") as file:
                self._player = pickle.load(file)
            self._view.textbox.set_text(messages.LOAD_SUCCESS)
        else:
            self._view.textbox.set_text(messages.LOAD_NOT_FOUND)

    def _cheat(self):

        # update model

        self._player.inventory[CardNames.FOOD].quantity += 5
        self._player.inventory[CardNames.WATER].quantity += 5

        # update view

        self._view.textbox.set_text(
            "You pressed the cheat key.\n"
            "Got 5 food card.\n"
            "Got 5 water card."
        )

        # TODO: duplicate code (game over checking)
        if self._player.has_won():
            self.game_running = False
            # TODO: stop game more quickly

    def _draw_card(self):
        if self._player.money >= PRICE_PER_CARD:

            self._player.money -= PRICE_PER_CARD

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

            self._player.inventory[card].quantity += 1

            text = "Got %s card." % card.name

            if card == CardNames.SSR:
                text = "GOT SSR CARD!!!"
            elif card not in SUPPLY:
                # TODO: decrease sanity by a random amount
                ...

            self._view.textbox.set_text(text)

        else:  # player.money < PRICE_PER_CARD
            self._view.textbox.set_text(
                "You do not have enough money!",
            )

        # TODO: duplicate code (game over checking)
        if self._player.has_won():
            self.game_running = False
            # TODO: stop game more quickly

    def _end_today(self):

        # update model

        self._player.sleep()

        # update view

        msg = (
            f"*** Day {self._player.age:02d} ***\n"
            f"HP -= {self._player.HP_decrease_per_day}\n"
            f"MP -= {self._player.MP_decrease_per_day}\n"
        )

        self._view.textbox.set_text(msg)

        # TODO: duplicate code (game over checking)
        if self._player.is_dead():
            self.game_running = False
            # TODO: stop game more quickly

    def _eat_food(self):
        # update model
        self._player.eat_food()

        # update view
        self._view.textbox.set_text("You ate some food.")

    def _drink_water(self):
        # update model
        self._player.drink_water()

        # update view
        self._view.textbox.set_text("You drank some water.")

    def _update_default_message(self):
        """
        根据当前的选中的 SideBar 选项或 ItemList 项目决定显示的帮助信息

        NOTE:
        如果想要给 Textbox 设定自定义信息，
        直接调用 Textbox.set_text 即可
        """

        option = self._view.sidebar.options[self._view.sidebar.selected_option_index]
        match self._view.mode:
            case ViewMode.LEVEL_1:
                match option:
                    case SideBarOptions.END_TODAY:
                        text = messages.END_TODAY
                    case SideBarOptions.INVENTORY:
                        text = messages.INVENTORY
                    case SideBarOptions.SHOP:
                        text = messages.SHOP
                    case SideBarOptions.SKILLS:
                        text = messages.SKILLS
                    case SideBarOptions.ABOUT:
                        text = messages.ABOUT
            case ViewMode.LEVEL_2:
                match self._view.item_list.mode:
                    case ItemListMode.INVENTORY:
                        match self._view.item_list.selected_item_index:
                            case InventoryItemIndex.SSR:
                                text = messages.SSR
                            case InventoryItemIndex.FOOD:
                                text = messages.FOOD
                            case InventoryItemIndex.WATER:
                                text = messages.WATER
                            case _:
                                text = messages.EXIT
                    case ItemListMode.SHOP:
                        ...
                    case ItemListMode.SKILLS:
                        item = self._view.item_list.items[self._view.item_list.selected_item_index]
                        name = item.item_name
                        if name in TALENT_POOL:
                            text = TALENT_DESC[name]
                        else:
                            text = messages.EXIT

        self._view.textbox.set_text(text)

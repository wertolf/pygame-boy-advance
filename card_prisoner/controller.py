import lega.draw
from card_prisoner import messages
from card_prisoner.constants import KEYDOWN_REPEAT_DELAY, KEYDOWN_INITIAL_DELAY, PRICE_PER_CARD, WINDOW_CAPTION
from card_prisoner.constants import (
    WIN_WIDTH,
    WIN_HEIGHT,
)
from card_prisoner.item_list import InventoryItemIndex, ItemListMode, ShopItemIndex
from card_prisoner.player import Player
from card_prisoner.sidebar import SideBarOptions
from card_prisoner.view import View, ViewMode
from card_prisoner.item import ITEM_DICT
from config import filenames, key_bindings
from lega.an import global_fadeout
from lega.misc import display_help, take_screenshot, terminate
from lega.screen import scrmgr
from card_prisoner.item import (
    SSR,
    A,
    B,
    C,
    FOOD,
    WATER,
    SUPPLY,
)
from card_prisoner.shop import Shop, N_ON_SALE_ITEMS_PER_DAY, N_WANTED_ITEMS_PER_DAY
from card_prisoner.item import Item, OnSaleItem, WantedItem, EMPTY_ITEM, SHOP_BARGAINER
from card_prisoner.constants import A_PROBABILITY, B_PROBABILITY


import pygame
from pygame.locals import KEYDOWN, KEYUP, QUIT


import logging
import os.path
import pickle
import random
import time

class GameController:
    def initialize_game(self):
        """
        initialization
        """

        # if __name__ == "__main__" the following steps are redundant
        # but if called from another script they may be necessary
        pygame.init()
        scrmgr.toggle_resolution((WIN_WIDTH, WIN_HEIGHT))
        scrmgr.clear_screen_without_update()
        scrmgr.update_global()

        # the following steps should all be necessary

        pygame.display.set_caption(WINDOW_CAPTION)

        # speed up event queue processing by only allowing relevant events on the queue
        # NOTE: in particular, mouse events are blocked in this game
        pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])

        # enable keyboard repeat
        # that is, held down keys will generate multiple KEYDOWN events
        # https://www.pygame.org/docs/ref/key.html#pygame.key.set_repeat
        pygame.key.set_repeat(KEYDOWN_INITIAL_DELAY, KEYDOWN_REPEAT_DELAY)

        # initialize model

        self._player = Player()
        is_bargainer = SHOP_BARGAINER in [talent.item_name for talent in self._player.talents]
        self._shop = Shop(is_bargainer)

        # initialize view
        self._view = View()
        self._update_sidebar()
        self._update_item_list()
        self._update_textbox_message()
        self._view.draw_everything()

        # following are main loop variables

        self.game_running = True

    def start_game(self):

        while self.game_running:

            for e in pygame.event.get():

                if e.type == QUIT:
                    terminate()

                elif e.type == KEYDOWN:

                    key = getattr(e, "key")

                    if key == key_bindings.RETURN_TO_TITLE:
                        restart_game = False
                        return restart_game

                    elif key == key_bindings.PRINT_SCREEN:
                        take_screenshot()

                    elif key == key_bindings.CHEAT:
                        self._cheat()

                    elif key == key_bindings.DRAW_CARD:
                        self._draw_card()
                
                    elif key in key_bindings.ARROW_KEYS:
                        self._on_arrow_key_up(key)

                    elif key == key_bindings.CONFIRM:
                        self._on_confirm()

                    elif key == key_bindings.CANCEL:
                        self._on_cancel()

                    elif key == key_bindings.SAVE_GAME:
                        self._save_game()

                    elif key == key_bindings.LOAD_GAME:
                        self._load_game()

                    elif key == key_bindings.DISPLAY_HELP:
                        display_help(messages.HELP)

                    else:
                        logging.critical(f"Ignored KEYDOWN: {key}")
                
                # end of event handling

            # 由于大多数事件都会修改 view 的某个局部
            # 所以出于简化的考虑，在循环末尾用一行代码可以省去在每一处都添加一行相同的代码
            # 唯一的影响是即使没有事件也会进行重绘
            # 但是这个问题可以在设定一个合适的 FPS 之后被后面的 tick 减轻
            self._view.draw_everything()

            scrmgr.tick()

            # end of main loop

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
        
        self._update_textbox_message()

    def _on_confirm(self):
        """
        为了减少 start_game 方法的行数而进行的封装
        类似于一个事件处理器，但是并不存在一个 CONFIRM 事件
        """
        sidebar = self._view.sidebar
        item_list = self._view.item_list
        option = sidebar.options[sidebar.selected_option_index]
        match self._view.mode:
            case ViewMode.LEVEL_1:
                match option:
                    case SideBarOptions.END_TODAY:
                        self._end_today()

                    case SideBarOptions.INVENTORY:
                        # TODO: duplicate code
                        self._view.mode = ViewMode.LEVEL_2
                        item_list.mode = ItemListMode.INVENTORY
                        item_list.selected_item_index = 0
                        self._update_item_list()
                    case SideBarOptions.SHOP:
                        # TODO: duplicate code
                        self._view.mode = ViewMode.LEVEL_2
                        item_list.mode = ItemListMode.SHOP
                        item_list.selected_item_index = 0
                        self._update_item_list()
                    case SideBarOptions.TALENT:
                        # TODO: duplicate code
                        self._view.mode = ViewMode.LEVEL_2
                        item_list.mode = ItemListMode.TALENT
                        item_list.selected_item_index = 0
                        self._update_item_list()
                    case _:
                        logging.critical(f"Got unsupported action: {option}")
            case ViewMode.LEVEL_2:
                item = item_list.items[item_list.selected_item_index]
                name = item.item_name
                match item_list.mode:
                    case ItemListMode.INVENTORY:
                        if name == FOOD:
                            self._eat_food()
                        elif name == WATER:
                            self._drink_water()
                        else:
                            self._view.textbox.set_text("This item cannot be used.")
                            return  # ad hoc solution: skip _update_textbox_message at the end of this function
                    case ItemListMode.SHOP:
                        self._buy_or_sell(item)
                        return  # ad hoc solution: skip _update_textbox_message at the end of this function
            case _:
                raise AssertionError(f"Got unexpected view mode: {self._view.mode}")

        self._update_textbox_message()

    def _on_cancel(self):
        """
        为了与 on_confirm 构成互补而进行的封装
        """
        if self._view.mode == ViewMode.LEVEL_2:
            self._view.mode = ViewMode.LEVEL_1
            self._view.item_list.mode = ItemListMode.EMPTY
            self._update_item_list()
            self._update_textbox_message()

    def _save_game(self):
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

    def _load_game(self):
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

        self._update_item_list()
        self._update_sidebar()

    def _cheat(self):

        # update model

        self._player.inventory[FOOD].quantity += 5
        self._player.inventory[WATER].quantity += 5

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
        player = self._player
        if player.money >= PRICE_PER_CARD:

            player.money -= PRICE_PER_CARD

            number = random.random()
            if number < player.SSR_probability:
                # 抽到 SSR 卡
                card = SSR
            elif number < (player.SSR_probability + player.SUPPLY_probability):
                # 抽到补给类卡
                # 具体抽到哪种，概率相同
                card = random.choice(SUPPLY)
            else:
                # 抽到普通卡
                number = random.random()
                if number < A_PROBABILITY:
                    card = A
                elif number < (A_PROBABILITY + B_PROBABILITY):
                    card = B
                else:
                    card = C

            self._player.inventory[card].quantity += 1

            text = "Got %s." % card

            if card == SSR:
                text = "GOT SSR CARD!!!"
            elif card not in SUPPLY:
                # TODO: decrease sanity by a random amount
                ...

            self._view.textbox.set_text(text)
            self._update_sidebar()

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

        self._shop.refresh_items()

        # update view

        msg = (
            f"*** Day {self._player.age:02d} ***\n"
            f"HP -= {self._player.HP_decrease_per_day}\n"
            f"MP -= {self._player.MP_decrease_per_day}\n"
        )

        self._view.textbox.set_text(msg)
        self._update_sidebar()

        # TODO: duplicate code (game over checking)
        if self._player.is_dead():
            self.game_running = False
            # TODO: stop game more quickly

    def _eat_food(self):
        # update model
        self._player.eat_food()

        # update view
        self._view.textbox.set_text("You ate some food.")
        self._update_sidebar()

    def _drink_water(self):
        # update model
        self._player.drink_water()

        # update view
        self._view.textbox.set_text("You drank some water.")
        self._update_sidebar()

    def _update_textbox_message(self):
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
                    case SideBarOptions.TALENT:
                        text = messages.TALENT
                    case SideBarOptions.ABOUT:
                        text = messages.ABOUT
            case ViewMode.LEVEL_2:
                item = self._view.item_list.items[self._view.item_list.selected_item_index]
                name = item.item_name

                # even empty items are instances of Item(EMPTY_ITEM)
                assert name in ITEM_DICT.keys()

                if self._view.item_list.mode == ItemListMode.SHOP:
                    if isinstance(item, OnSaleItem):
                        title = "ITEM ON SALE"
                        desc = (
                            f"Give me {item.price.quantity} {item.price.item_name}s.\n"
                            f"I will give you {item.quantity} {name}s in return."
                        )
                    elif isinstance(item, WantedItem):
                        title = "ITEM WANTED"
                        desc = (
                            f"Give me {item.quantity} {name}.\n"
                            f"I will give you ${item.price}."
                        )
                    else:
                        assert name == EMPTY_ITEM
                        title = name.upper()
                        desc = ITEM_DICT[name]["desc"]
                else:
                    title = name.upper()
                    desc = ITEM_DICT[name]["desc"]

                # 在这里可以按照自己的想法定义帮助文本的显示格式
                text = (
                    f"{title}\n"
                    "\n"
                    f"{desc}"  # description
                )

        self._view.textbox.set_text(text)

    def _update_item_list(self):
        items = [Item()] * self._view.item_list.n_cols * self._view.item_list.n_rows

        match self._view.item_list.mode:
            case ItemListMode.EMPTY:
                pass
            case ItemListMode.INVENTORY:
                items[InventoryItemIndex.SSR] = self._player.inventory[SSR]
                items[InventoryItemIndex.A] = self._player.inventory[A]
                items[InventoryItemIndex.B] = self._player.inventory[B]
                items[InventoryItemIndex.C] = self._player.inventory[C]
                items[InventoryItemIndex.FOOD] = self._player.inventory[FOOD]
                items[InventoryItemIndex.WATER] = self._player.inventory[WATER]
            case ItemListMode.SHOP:
                for i in range(N_ON_SALE_ITEMS_PER_DAY):
                    items[i + ShopItemIndex.ON_SALE_ITEM_1] = \
                        self._shop.on_sale_items[i]
                for i in range(N_WANTED_ITEMS_PER_DAY):
                    items[i + ShopItemIndex.WANTED_ITEM_1] = \
                        self._shop.wanted_items[i]
            case ItemListMode.TALENT:
                items[0] = self._player.talents[0]
                items[1] = self._player.talents[1]
        
        self._view.item_list.items = items

    def _update_sidebar(self):
        sidebar = self._view.sidebar
        player = self._player

        sidebar.day = player.age
        sidebar.money_value = player.money
        sidebar.HP_value = player.HP
        sidebar.MP_value = player.MP

    def _buy_or_sell(self, item):
        player = self._player
        if isinstance(item, OnSaleItem):
            if player.inventory[item.price.item_name].quantity < item.price.quantity:
                self._view.textbox.set_text(f"You do not have enough {item.price.item_name}s!")
            else:
                player.inventory[item.price.item_name].quantity -= item.price.quantity
                player.inventory[item.item_name].quantity += item.quantity

                item_index = self._shop.on_sale_items.index(item)
                self._shop.on_sale_items[item_index] = Item(EMPTY_ITEM)
                self._update_item_list()

                self._view.textbox.set_text("Thanks.")
        elif isinstance(item, WantedItem):
            if player.inventory[item.item_name].quantity < item.quantity:
                self._view.textbox.set_text(f"You do not have enough {item.item_name}s!")
            else:
                player.inventory[item.item_name].quantity -= item.quantity
                player.money += item.price
                self._update_sidebar()

                # 不同于 on sale
                # wanted item 可以一直存在，即交易的次数不受限制

                self._view.textbox.set_text("Thanks.")

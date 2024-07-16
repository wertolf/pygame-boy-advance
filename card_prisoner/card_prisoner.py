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


def cheat(view: View, player: Player):
    player.inventory[CardNames.FOOD].quantity += 5
    player.inventory[CardNames.WATER].quantity += 5

    view.textbox.set_text(
        "You pressed the cheat key.\n"
        "Got 5 food card.\n"
        "Got 5 water card."
    )


def eat_food(view: View, player: Player):
    # update model
    player.eat_food()

    # update view
    view.textbox.set_text("You ate some food.")


def drink_water(view: View, player: Player):
    # update model
    player.drink_water()

    # update view
    view.textbox.set_text("You drank some water.")


def draw_card(view: View, player: Player):
    if player.money >= PRICE_PER_CARD:

        player.money -= PRICE_PER_CARD

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

        player.inventory[card].quantity += 1

        text = "Got %s card." % card.name

        if card == CardNames.SSR:
            text = "GOT SSR CARD!!!"
        elif card not in SUPPLY:
            # TODO: decrease sanity by a random amount
            ...

        view.textbox.set_text(text)

    else:  # player.money < PRICE_PER_CARD
        view.textbox.set_text(
            "You do not have enough money!",
        )


def end_today(view: View, player: Player):

    # update model

    player.sleep()

    # update view

    view.sidebar_index = view.sidebar_index  # call action_index.setter to update inventory properly

    msg = (
        f"*** Day {player.age:02d} ***\n"
        f"HP -= {player.HP_decrease_per_day}\n"
        f"MP -= {player.MP_decrease_per_day}\n"
    )

    view.textbox.set_text(msg)

def start_game():

    # initialization

    # if __name__ == "__main__" the following steps are redundant
    # but if called from another script they may be necessary
    pygame.init()
    scrmgr.clear_screen_without_update()
    scrmgr.update_global()

    pygame.display.set_caption(WINDOW_CAPTION)

    player = Player()
    view = View()

    view.draw_everything(player)

    # main loop

    game_running = True
    pressed_key = None
    is_holding_key = False
    key_holding_timer = 0
    draw_card_timer = 0
    KEYDOWN_INITIAL_INTERVAL = 1  # seconds
    DRAW_CARD_TIME_INTERVAL = 0.1  # seconds
    while game_running:

        # timer-related logic

        if pressed_key is not None:
            # 若某个键处于被按下的状态

            if not is_holding_key:
                # 若它还没有进入长按状态，则判断是否可以进入长按状态
                time_elapsed = time.time() - key_holding_timer
                if time_elapsed > KEYDOWN_INITIAL_INTERVAL:
                    is_holding_key = True
            else:
                # 若已经进入长按状态，则重复执行该键对应的行为
                match pressed_key:
                    case key_bindings.DRAW_CARD:
                        time_elapsed = time.time() - draw_card_timer
                        if time_elapsed > DRAW_CARD_TIME_INTERVAL:
                            # TODO: duplicate code in KEYDOWN handler
                            draw_card(view, player)

                            # TODO: duplicate code in KEYDOWN handler
                            if player.has_won():
                                game_running = False
                                break
                                
                            draw_card_timer = time.time()
                    case _:
                        logging.critical(f"Got unsupported key holding: {pressed_key}")

        # event handling

        for e in pygame.event.get():
            if e.type == QUIT:
                terminate()
            elif e.type == KEYDOWN:

                # 用于识别长按
                key_holding_timer = time.time()

                key = getattr(e, "key")
                match key:
                    case key_bindings.DRAW_CARD:
                        # 按下 D 键时立刻进行一次抽卡
                        # 如果持续按住 KEYDOWN_INITIAL_TIME_INTERVAL
                        # 则之后每隔 DRAW_CARD_TIME_INTERVAL 抽一次卡
                        draw_card(view, player)

                        # TODO: duplicate code (game over checking)
                        if player.has_won():
                            game_running = False
                            break
                            
                        pressed_key = key_bindings.DRAW_CARD
                        draw_card_timer = time.time()
            elif e.type == KEYUP:

                # 重置用于识别长按的相关数据结构
                is_holding_key = False
                pressed_key = None

                key = getattr(e, "key")
                option = view.sidebar.options[view.sidebar_index]
                if key == key_bindings.RETURN_TO_TITLE:
                    restart_game = False
                    return restart_game
                elif key == key_bindings.PRINT_SCREEN:
                    take_screenshot()
                elif key == key_bindings.CHEAT:
                    cheat(view, player)

                    # TODO: duplicate code (game over checking)
                    if player.has_won():
                        game_running = False
                        break
                elif key == key_bindings.DRAW_CARD:
                    pass

                elif key == key_bindings.CONFIRM:
                    match view.mode:
                        case ViewMode.LEVEL_1:
                            match option:
                                case SideBarOptions.END_TODAY:
                                    end_today(view, player)

                                    if player.is_dead():
                                        game_running = False
                                        break
                                case SideBarOptions.INVENTORY:
                                    view.mode = ViewMode.LEVEL_2
                                case SideBarOptions.SHOP:
                                    view.mode = ViewMode.LEVEL_2
                                case SideBarOptions.SKILLS:
                                    view.mode = ViewMode.LEVEL_2
                                case _:
                                    logging.critical(f"Got unsupported action: {option}")
                        case ViewMode.LEVEL_2:
                            match view.item_list.mode:
                                case ItemListMode.INVENTORY:
                                    match view.item_list_index:
                                        case InventoryItemIndex.FOOD:
                                            eat_food(view, player)
                                        case InventoryItemIndex.WATER:
                                            drink_water(view, player)
                                        case _:
                                            logging.critical(f"unsupported")
                                case ItemListMode.SHOP:
                                    match view.item_list_index:
                                        case ShopItemIndex.DRAW_1_CARD:
                                            draw_card(view, player)
                                        case _:
                                            logging.critical(f"unsupported")
                        case _:
                            raise AssertionError(f"Got unexpected view mode: {view.mode}")
                elif key == key_bindings.CANCEL:
                    if view.mode == ViewMode.LEVEL_2:
                        view.mode = ViewMode.LEVEL_1
                elif key == key_bindings.UP:
                    if view.mode == ViewMode.LEVEL_1:
                        # 注意 actions 列表是自底向上的
                        # 所以 up 会增加索引值
                        # down 会减少索引值
                        view.sidebar_index += 1
                    elif view.mode == ViewMode.LEVEL_2:
                        view.item_list_index -= view.item_list.n_cols

                elif key == key_bindings.DOWN:
                    if view.mode == ViewMode.LEVEL_1:
                        view.sidebar_index -= 1
                    elif view.mode == ViewMode.LEVEL_2:
                        view.item_list_index += view.item_list.n_cols
                
                elif key == key_bindings.LEFT:
                    if view.mode == ViewMode.LEVEL_2:
                        view.item_list_index -= 1

                elif key == key_bindings.RIGHT:
                    if view.mode == ViewMode.LEVEL_2:
                        view.item_list_index += 1

                elif key == key_bindings.SAVE_GAME:

                    # PROGRAM_DATA_DIR is created in pygame_boy_advance.py
                    assert os.path.exists(filenames.PROGRAM_DATA_DIR)

                    with open(filenames.CARD_PRISONER_SAVE_FILE, "wb") as file:
                        pickle.dump(player, file)
                    view.textbox.set_text(messages.SAVE_SUCCESS)

                elif key == key_bindings.LOAD_GAME:
                    filename = filenames.CARD_PRISONER_SAVE_FILE
                    if os.path.exists(filename):
                        with open(filename, "rb") as file:
                            player = pickle.load(file)
                        view.textbox.set_text(messages.LOAD_SUCCESS)
                    else:
                        view.textbox.set_text(messages.LOAD_NOT_FOUND)
                
                elif key == key_bindings.DISPLAY_HELP:
                    display_help(messages.HELP)
                else:
                    logging.critical(f"Ignored KEYUP: {key}")

        # 由于大多数事件都会修改 view 的某个局部
        # 所以出于简化的考虑，在循环末尾用一行代码可以省去在每一处都添加一行相同的代码
        # 唯一的影响是即使没有事件也会进行重绘
        # 但是这个问题可以在设定一个合适的 FPS 之后被后面的 tick 减轻
        view.draw_everything(player)

        scrmgr.tick()

    assert player.is_game_over()

    global_fadeout()  # 全局淡出
    if player.has_won():
        msg = (
            "Congratulations! You won!"
        )
    elif player.is_dead():
        msg = player.death_reason
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

def main():
    restart_game = True
    while restart_game:
        restart_game = start_game()


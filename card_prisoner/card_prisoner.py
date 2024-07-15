import pygame
import pygame.draw
from pygame.locals import QUIT
from pygame.locals import KEYUP, KEYDOWN

from card_prisoner.model.player import Player
from card_prisoner.view.view import View
from card_prisoner.view.view import ViewMode
from card_prisoner.view.item_list import InventoryItemIndex, ShopItemIndex, ItemListMode
from card_prisoner.view.sidebar import SideBarOptions
from card_prisoner import actions, animations
from card_prisoner.shared import messages
from lega.screen import scrmgr

from lega.misc import terminate

import lega.draw

from config import filenames, key_bindings, color_theme

import time
import logging
import pickle
import os.path
import math

WINDOW_CAPTION = "Card Prisoner"

def display_help_message(page_index):
    scrmgr.clear_screen_without_update()

    # 绘制帮助文本

    lega.draw.text_multi_line(
        scrmgr.screen,
        messages.HELP[page_index],
        reference_point=scrmgr.center,
    )

    # 绘制两个等边三角形

    length = scrmgr.win_width / 16 / 4  # 等边三角形的边长
    padding_x = scrmgr.win_width / 16  # 与窗口左右边缘的距离

    pygame.draw.polygon(
        scrmgr.screen,
        color_theme.foreground,
        [
            (padding_x, scrmgr.center.y),
            (padding_x + length * math.sqrt(3) / 2, scrmgr.center.y - length / 2),
            (padding_x + length * math.sqrt(3) / 2, scrmgr.center.y + length / 2),
        ]
    )

    pygame.draw.polygon(
        scrmgr.screen,
        color_theme.foreground,
        [
            (scrmgr.win_width - padding_x, scrmgr.center.y),
            (scrmgr.win_width - padding_x - length * math.sqrt(3) / 2, scrmgr.center.y - length / 2),
            (scrmgr.win_width - padding_x - length * math.sqrt(3) / 2, scrmgr.center.y + length / 2),
        ]
    )

    # 绘制页面底部文本

    padding_bottom = scrmgr.win_width / 16 / 4  # 与窗口底部的距离

    lega.draw.text_single_line(
        scrmgr.screen,
        messages.HELP_BOTTOM,
        centerx=scrmgr.center.x, centery=scrmgr.win_height - padding_bottom,
    )

    scrmgr.update_global()

def help_subpage():

    # init
    help_page_index = 0
    display_help_message(help_page_index)

    while True:  # 在单独的函数中进行单独的事件处理
        for e in pygame.event.get():
            if e.type == QUIT:
                terminate()
            elif e.type == KEYUP:
                key = getattr(e, "key")
                match key:
                    case key_bindings.cancel:
                        return
                    case key_bindings.left:
                        help_page_index = (help_page_index - 1) % len(messages.HELP)
                        display_help_message(help_page_index)
                    case key_bindings.right:
                        help_page_index = (help_page_index + 1) % len(messages.HELP)
                        display_help_message(help_page_index)
        
        scrmgr.tick()



def start_game():

    # initialization

    # if __name__ == "__main__" the following steps are redundant
    # but if called from another script they may be necessary
    pygame.init()
    scrmgr.clear_screen_without_update()

    pygame.display.set_caption(WINDOW_CAPTION)

    player = Player()
    view = View()

    view.draw_everything(player)
    scrmgr.update_global()

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
                    case key_bindings.draw_card:
                        time_elapsed = time.time() - draw_card_timer
                        if time_elapsed > DRAW_CARD_TIME_INTERVAL:
                            # TODO: duplicate code in KEYDOWN handler
                            actions.draw_card(view, player)

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
                    case key_bindings.draw_card:
                        # 按下 D 键时立刻进行一次抽卡
                        # 如果持续按住 KEYDOWN_INITIAL_TIME_INTERVAL
                        # 则之后每隔 DRAW_CARD_TIME_INTERVAL 抽一次卡
                        actions.draw_card(view, player)

                        # TODO: duplicate code (game over checking)
                        if player.has_won():
                            game_running = False
                            break
                            
                        pressed_key = key_bindings.draw_card
                        draw_card_timer = time.time()
            elif e.type == KEYUP:

                # 重置用于识别长按的相关数据结构
                is_holding_key = False
                pressed_key = None

                key = getattr(e, "key")
                option = view.sidebar.options[view.sidebar_option_index]
                if key == key_bindings.cheat:
                    actions.cheat(view, player)

                    # TODO: duplicate code (game over checking)
                    if player.has_won():
                        game_running = False
                        break
                elif key == key_bindings.draw_card:
                    pass

                elif key == key_bindings.confirm:
                    match view.mode:
                        case ViewMode.LEVEL_1:
                            match option:
                                case SideBarOptions.BACK:
                                    return False
                                case SideBarOptions.END_TODAY:
                                    actions.end_today(view, player)

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
                                            actions.eat_food(view, player)
                                        case InventoryItemIndex.WATER:
                                            actions.drink_water(view, player)
                                        case _:
                                            logging.critical(f"unsupported")
                                case ItemListMode.SHOP:
                                    match view.item_list_index:
                                        case ShopItemIndex.DRAW_1_CARD:
                                            actions.draw_card(view, player)
                                        case _:
                                            logging.critical(f"unsupported")
                        case _:
                            raise AssertionError(f"Got unexpected view mode: {view.mode}")
                elif key == key_bindings.cancel:
                    if view.mode == ViewMode.LEVEL_2:
                        view.mode = ViewMode.LEVEL_1
                elif key == key_bindings.up:
                    if view.mode == ViewMode.LEVEL_1:
                        # 注意 actions 列表是自底向上的
                        # 所以 up 会增加索引值
                        # down 会减少索引值
                        view.sidebar_option_index += 1
                    elif view.mode == ViewMode.LEVEL_2:
                        view.item_list_index -= view.item_list.n_cols

                elif key == key_bindings.down:
                    if view.mode == ViewMode.LEVEL_1:
                        view.sidebar_option_index -= 1
                    elif view.mode == ViewMode.LEVEL_2:
                        view.item_list_index += view.item_list.n_cols
                
                elif key == key_bindings.left:
                    if view.mode == ViewMode.LEVEL_2:
                        view.item_list_index -= 1

                elif key == key_bindings.right:
                    if view.mode == ViewMode.LEVEL_2:
                        view.item_list_index += 1

                elif key == key_bindings.save:

                    # PROGRAM_DATA_DIR is created in pygame_boy_advance.py
                    assert os.path.exists(filenames.PROGRAM_DATA_DIR)

                    with open(filenames.CARD_PRISONER_SAVE_FILE, "wb") as file:
                        pickle.dump(player, file)
                    view.textbox.set_text(messages.SAVE_SUCCESS)

                elif key == key_bindings.load:
                    filename = filenames.CARD_PRISONER_SAVE_FILE
                    if os.path.exists(filename):
                        with open(filename, "rb") as file:
                            player = pickle.load(file)
                        view.textbox.set_text(messages.LOAD_SUCCESS)
                    else:
                        view.textbox.set_text(messages.LOAD_NOT_FOUND)
                
                elif key == key_bindings.show_help:
                    help_subpage()
                else:
                    logging.critical(f"Ignored KEYUP: {key}")

        # 由于大多数事件都会修改 view 的某个局部
        # 所以出于简化的考虑，在循环末尾用一行代码可以省去在每一处都添加一行相同的代码
        # 唯一的影响是即使没有事件也会进行重绘
        # 但是这个问题可以在设定一个合适的 FPS 之后被后面的 tick 减轻
        view.draw_everything(player)

        scrmgr.tick()

    assert player.is_game_over()

    if player.has_won():
        animations.victory_animation()
    elif player.is_dead():
        animations.game_over_animation()
    
    while True:
        for e in pygame.event.get():
            if e.type == QUIT:
                terminate()
            elif e.type == KEYUP:
                key = getattr(e, "key")
                if key == key_bindings.restart:
                    return True
        
        scrmgr.tick()

def main():
    restart_game = True
    while restart_game:
        restart_game = start_game()

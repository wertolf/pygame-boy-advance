import pygame
from pygame.locals import QUIT
from pygame.locals import KEYUP, KEYDOWN

from card_prisoner.model.player import Player
from card_prisoner.view.view import View
from card_prisoner.view.view import ViewMode
from card_prisoner.view.item_list import InventoryItemIndex, ShopItemIndex, ItemListMode
from card_prisoner.view.sidebar import SideBarOptions
from card_prisoner import actions
from lega.screen import scrmgr

from lega.misc import terminate

from config import key_binding

import time
import logging

def start_game():

    # initialization

    # if __name__ == "__main__" the following steps are redundant
    # but if called from another script they may be necessary
    pygame.init()
    scrmgr.clear_screen_without_update()

    pygame.display.set_caption("Card Prisoner")

    player = Player()
    view = View()

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
                    case key_binding.draw_card:
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
                    case key_binding.draw_card:
                        # 按下 D 键时立刻进行一次抽卡
                        # 如果持续按住 KEYDOWN_INITIAL_TIME_INTERVAL
                        # 则之后每隔 DRAW_CARD_TIME_INTERVAL 抽一次卡
                        actions.draw_card(view, player)

                        # TODO: duplicate code (game over checking)
                        if player.has_won():
                            game_running = False
                            break
                            
                        pressed_key = key_binding.draw_card
                        draw_card_timer = time.time()
            elif e.type == KEYUP:

                # 重置用于识别长按的相关数据结构
                is_holding_key = False
                pressed_key = None

                key = getattr(e, "key")
                option = view.sidebar.options[view.sidebar_option_index]
                if key == key_binding.cheat:
                    actions.cheat(view, player)

                    # TODO: duplicate code (game over checking)
                    if player.has_won():
                        game_running = False
                        break
                elif key == key_binding.draw_card:
                    pass

                elif key == key_binding.confirm:
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
                elif key == key_binding.cancel:
                    if view.mode == ViewMode.LEVEL_2:
                        view.mode = ViewMode.LEVEL_1
                elif key == key_binding.up:
                    if view.mode == ViewMode.LEVEL_1:
                        # 注意 actions 列表是自底向上的
                        # 所以 up 会增加索引值
                        # down 会减少索引值
                        view.sidebar_option_index += 1
                    elif view.mode == ViewMode.LEVEL_2:
                        view.item_list_index -= view.item_list.n_cols

                elif key == key_binding.down:
                    if view.mode == ViewMode.LEVEL_1:
                        view.sidebar_option_index -= 1
                    elif view.mode == ViewMode.LEVEL_2:
                        view.item_list_index += view.item_list.n_cols
                
                elif key == key_binding.left:
                    if view.mode == ViewMode.LEVEL_2:
                        view.item_list_index -= 1

                elif key == key_binding.right:
                    if view.mode == ViewMode.LEVEL_2:
                        view.item_list_index += 1

                else:
                    logging.critical(f"Ignored KEYUP: {key}")

        if view.global_update_needed:
            if not player.is_game_over():
                view.draw_everything(player)
            scrmgr.update_global()
            view.global_update_needed = False

    assert player.is_game_over()
    
    while True:
        for e in pygame.event.get():
            if e.type == QUIT:
                terminate()
            elif e.type == KEYUP:
                key = getattr(e, "key")
                if key == key_binding.restart:
                    return True

def main():
    restart_game = True
    while restart_game:
        restart_game = start_game()

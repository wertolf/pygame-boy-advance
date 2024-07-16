import pygame
import sys

from lega.screen import scrmgr

from pygame.locals import QUIT, KEYUP

from config import key_bindings, color_theme, filenames
import lega.draw
import math

import os.path
import logging


def terminate():
    pygame.quit()
    sys.exit()


def display_help(message_list):
    """
    显示帮助：一个拥有完整事件处理逻辑的独立子页面

    message_list: 一个 str 列表，每个 str 对应一页的文本内容，使用 \n 分隔不同行
    """

    # 嵌套函数
    # 其实拿出来也行，但是嵌套的话可以直接使用父函数的 message_list 变量
    def draw_help_page(page_index):
        scrmgr.clear_screen_without_update()

        BOTTOM_TEXT = "Press left/right to switch page. Press X to leave."

        # 绘制帮助文本

        lega.draw.text_multi_line(
            scrmgr.screen,
            message_list[page_index],
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
            BOTTOM_TEXT,
            centerx=scrmgr.center.x, centery=scrmgr.win_height - padding_bottom,
        )

        scrmgr.update_global()

        return  # end draw_help_page

    # initialization
    help_page_index = 0
    draw_help_page(help_page_index)

    while True:  # 在单独的函数中进行单独的事件处理
        for e in pygame.event.get():
            if e.type == QUIT:
                terminate()
            elif e.type == KEYUP:
                key = getattr(e, "key")
                match key:
                    case key_bindings.CANCEL:
                        return
                    case key_bindings.LEFT:
                        help_page_index = (help_page_index - 1) % len(message_list)
                        draw_help_page(help_page_index)
                    case key_bindings.RIGHT:
                        help_page_index = (help_page_index + 1) % len(message_list)
                        draw_help_page(help_page_index)
        
        scrmgr.tick()

def take_screenshot():
    filename = "screenshot.png"
    filename = os.path.join(filenames.PROGRAM_DATA_DIR, filename)
    pygame.image.save(scrmgr.screen, filename)
    logging.critical(f"Screenshot saved at {filename}.")


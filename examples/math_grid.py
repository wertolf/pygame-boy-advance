import pygame
import sys
import math
import numpy as np

from pygame import (
    Color,
    Surface,
    Rect,
)
from pygame.locals import (
    QUIT, MOUSEMOTION, KEYUP,
    K_PRINTSCREEN,
    SRCALPHA,
)

import os.path
import datetime
import logging
logging.basicConfig(level=logging.INFO)

# 创建画布
CANVAS_WIDTH = 1280
CANVAS_HEIGHT = 720
canvas = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT))

# 定义常用的长度和坐标
CENTERX = int(CANVAS_WIDTH / 2)
CENTERY = int(CANVAS_HEIGHT / 2)
DOT_RADIUS = int(CANVAS_WIDTH / 128)
PADDING = int(CANVAS_WIDTH / 16)
THIN = 1
THICK = THIN * 3
UNIT_LENGTH = int(CANVAS_WIDTH / 16)
ORIGIN = np.array((CENTERX, CENTERY))
I_HAT = np.array((UNIT_LENGTH, 0))  # (1, 0)
J_HAT = np.array((0, (-1) * UNIT_LENGTH))  # (0, 1)
Y_MAX = (CANVAS_HEIGHT / 2) / UNIT_LENGTH
Y_MIN = (-1) * Y_MAX
X_MAX = (CANVAS_WIDTH / 2) / UNIT_LENGTH
X_MIN = (-1) * X_MAX

# 设置前景色与背景色
WHITE = Color(255, 255, 255)
BLACK = Color(0, 0, 0)
YELLOW = Color(255, 255, 0)
RED = Color(255, 0, 0)
FOREGROUND = BLACK
BACKGROUND = WHITE
HIGHLIGHT = RED

# 存放截图的路径
PROGRAM_DATA = "program_data"

def draw_dot(center):
    """
    绘制原点
    """
    pygame.draw.circle(canvas, HIGHLIGHT, center, DOT_RADIUS)

def draw_line(start, end, thickness, color=FOREGROUND):
    pygame.draw.line(canvas, color, start, end, thickness)

def draw_axes():
    """
    绘制坐标轴
    """
    arrow_angle = math.radians(30)  # 箭头的一侧与坐标轴的夹角
    arrow_length = int(CANVAS_WIDTH / 64)  # 箭头一侧的长度

    # 绘制 x 轴
    x_start = (PADDING, CENTERY)
    x_end = (CANVAS_WIDTH - PADDING, CENTERY)
    draw_line(x_start, x_end, THICK)
    # 绘制箭头
    # arrow_end = [
    #     x_end[0] - arrow_length * math.cos(arrow_angle),
    #     x_end[1] - arrow_length * math.sin(arrow_angle),
    # ]
    # draw_line(x_end, arrow_end, THICK)
    # arrow_end[1] = x_end[1] + arrow_length * math.sin(arrow_angle)
    # draw_line(x_end, arrow_end, THICK)

    # 绘制 y 轴
    y_start = (CENTERX, CANVAS_HEIGHT - PADDING)
    y_end = (CENTERX, PADDING)
    draw_line(y_start, y_end, THICK)
    # # 绘制箭头
    # arrow_end = [
    #     y_end[0] - arrow_length * math.sin(arrow_angle),
    #     y_end[1] + arrow_length * math.cos(arrow_angle),
    # ]
    # draw_line(y_end, arrow_end, THICK)
    # arrow_end[0] = y_end[0] + arrow_length * math.sin(arrow_angle)
    # draw_line(y_end, arrow_end, THICK)

def draw_grid():
    N_COLS = int((CANVAS_WIDTH / 2) / UNIT_LENGTH)
    N_ROWS = int((CANVAS_HEIGHT / 2) / UNIT_LENGTH)

    # 绘制横线
    for y in range((-1) * N_ROWS, N_ROWS + 1):
        y = CENTERY + y * UNIT_LENGTH
        start = (0, y)
        end = (CANVAS_WIDTH, y)
        draw_line(start, end, THIN)

    # 绘制竖线
    for x in range((-1) * N_COLS, N_COLS + 1):
        x = CENTERX + x * UNIT_LENGTH
        start = (x, CANVAS_HEIGHT)
        end = (x, 0)
        draw_line(start, end, THIN)

def draw_kx(slope, intercept=0):
    """
    绘制 y = kx + b
    """
    # TODO: 判断线段率先触碰到上下边框还是左右边框
    start = (
        X_MIN,
        slope * X_MIN + intercept,
    )
    start = screen2board(start)
    end = (
        X_MAX,
        slope * X_MAX + intercept,
    )
    end = screen2board(end)
    draw_line(start, end, THICK, color=HIGHLIGHT)

def screen2board(coord):
    """
    将屏幕坐标转换为棋盘坐标
    """
    return ORIGIN + I_HAT * coord[0] + J_HAT * coord[1]

def board2screen(coord):
    """
    将棋盘坐标转换为屏幕坐标
    """
    # TODO: 目前的实现方式不够优雅
    return (
        (coord[0] - ORIGIN[0]) / UNIT_LENGTH,
        (coord[1] - ORIGIN[1]) / UNIT_LENGTH * (-1),
    )

def terminate():
    pygame.quit()
    sys.exit()

def main():
    canvas.fill(BACKGROUND)
    # draw_grid()
    draw_axes()
    draw_dot(ORIGIN)
    background_layer = canvas.copy()

    running = True
    clock = pygame.time.Clock()
    fps = 10
    while running:
        for e in pygame.event.get():
            if e.type == QUIT:
                terminate()
            # elif e.type == MOUSEMOTION:
            #     pos = getattr(e, "pos")
            #     coord = board2screen(pos)
            #     # 之所以减 0 是因为原点的坐标是 (0, 0)
            #     k = (coord[1] - 0) / (coord[0] - 0)
            #     # TODO: 处理分母为零的情况

            #     canvas.blit(background_layer, (0, 0))
            #     draw_dot(pos)
            #     draw_kx(k)
            elif e.type == KEYUP:
                key = getattr(e, "key")
                if key == K_PRINTSCREEN:
                    now = datetime.datetime.now()
                    timestamp = now.strftime(r"%Y-%m-%d_%H%M%S")
                    filename = f"screenshot_{timestamp}.png"
                    path = os.path.join(PROGRAM_DATA, filename)
                    pygame.image.save(canvas, path)
                    logging.info(f"Screenshot saved at {path}.")
        pygame.display.update()
        clock.tick(fps)

if __name__ == "__main__":
    main()

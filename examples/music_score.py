import pygame
import sys
import math

from pygame import (
    Color,
    Surface,
    Rect,
)
from pygame.locals import (
    QUIT,
    SRCALPHA,
)

# 创建画布
CANVAS_WIDTH = 1280
CANVAS_HEIGHT = 720
canvas = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT))

# 定义常用的坐标和长度
CENTERX = CANVAS_WIDTH / 2
CENTERY = CANVAS_HEIGHT / 2
LINE_DISTANCE = CANVAS_HEIGHT / 9
LINE_WIDTH = CANVAS_WIDTH / 2
LINE_THICKNESS = 5
N_LINES = 5
NOTE_WIDTH = LINE_DISTANCE * 1.25
NOTE_HEIGHT = LINE_DISTANCE

# 设置前景色与背景色
WHITE = Color(255, 255, 255)
BLACK = Color(0, 0, 0)
FOREGROUND = WHITE
BACKGROUND = BLACK


def draw_crotchet():
    """
    绘制四分音符
    """

    # 绘制符头
    head = Surface(
        (NOTE_WIDTH, NOTE_HEIGHT),
        SRCALPHA,
    )
    pygame.draw.ellipse(head, FOREGROUND, head.get_rect())

    rotation = 30
    head = pygame.transform.rotate(head, rotation)

    rect = head.get_rect(
        centerx=CENTERX,
        centery=CENTERY,
    )
    canvas.blit(head, rect)

    # 绘制符尾
    stem = LINE_DISTANCE * 3.5
    pygame.draw.line(
        canvas, FOREGROUND,
        (rect.right, rect.centery),
        (rect.right, rect.centery - stem),
        LINE_THICKNESS,
    )

def draw_lines():
    """
    以 CENTERY 为中心绘制五条线段
    """
    start_x = CENTERX - LINE_WIDTH / 2  # 线段起点的横坐标
    end_x = CENTERX + LINE_WIDTH / 2  # 线段终点的横坐标

    y = CENTERY - LINE_DISTANCE * math.floor(N_LINES / 2)
    for _ in range(N_LINES):
        start_pos = (start_x, y)
        end_pos = (end_x, y)
        pygame.draw.line(canvas, FOREGROUND, start_pos, end_pos, LINE_THICKNESS)
        y += LINE_DISTANCE

def terminate():
    pygame.quit()
    sys.exit()

def main():
    draw_lines()
    draw_crotchet()

    running = True
    clock = pygame.time.Clock()
    fps = 10
    while running:
        for e in pygame.event.get():
            if e.type == QUIT:
                terminate()
        pygame.display.update()
        clock.tick(fps)

if __name__ == "__main__":
    main()

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

    a = NOTE_WIDTH  # 椭圆的半长轴
    b = NOTE_HEIGHT  # 椭圆的半短轴

    # 我们希望最终绘制的椭圆沿中心逆时针旋转的度数
    rotation_angle = 30  # theta (in degree)
    theta = math.radians(rotation_angle)
    k = math.tan(math.pi / 2 - theta)  # 切线斜率
    # 使用高中学过的解析几何知识，联立椭圆方程与切线方程，计算切点坐标
    # 已知切线与 x 轴正方向的夹角为 (90 - rotation_angle) 度
    # 且切点限制在第 4 象限
    # 假设椭圆的中心坐标为 (0, 0)
    intercept = (-1) * math.sqrt(k**2 * a**2 + b**2)  # 切线的截距
    tangency_point = (  # 切点坐标
        k * a**2 / abs(intercept),
        (-1) * b**2 / abs(intercept),
    )
    # i_hat: 将 x 轴的单位向量 (1, 0) 逆时针旋转 theta 所得向量
    i_hat = (
        math.cos(theta),
        math.sin(theta),
    )
    # j_hat: 将 y 轴的单位向量 (0, 1) 逆时针旋转 theta 所得向量
    j_hat = (
        (-1) * math.sin(theta),
        math.cos(theta),
    )
    # 完成上述旋转所需要的矩阵/线性变换
    transformation = np.array([i_hat, j_hat]).swapaxes(0, 1)
    # 经过旋转之后得到的切点坐标
    tangency_point = transformation @ tangency_point

    # 绘制符头
    head = Surface(
        (a, b),
        SRCALPHA,
    )
    pygame.draw.ellipse(head, FOREGROUND, head.get_rect())

    # 将逆时针旋转 rotation_angle 度
    head = pygame.transform.rotate(head, rotation_angle)

    # 符头在屏幕上的位置信息
    centerx = CENTERX
    centery = CENTERY

    rect = head.get_rect(
        centerx=centerx,
        centery=centery,
    )
    canvas.blit(head, rect)

    # 符尾在屏幕上的位置
    x = centerx + tangency_point[0]  # TODO: this is not correct
    y = centery - tangency_point[1]  # 之所以用减法是因为屏幕坐标系的 y 轴方向朝下

    # 绘制符尾
    stem = LINE_DISTANCE * 3.5
    pygame.draw.line(
        canvas, FOREGROUND,
        (x, y),
        (x, y - stem),  # 减法表示向上
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

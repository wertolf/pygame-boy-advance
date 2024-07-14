"""
Simple Animations
"""

from lega.screen import scrmgr

import pygame.time

MAX_ALPHA = 255
MIN_ALPHA = 0

LEFT_TOP_CORNER = (0, 0)

DEFAULT_TIME_DELAYED = 1000  # ms
DEFAULT_FADEOUT_SPEED = 5

def global_fadeout(**kwargs):
    """
    * 简化设计：只支持全屏淡出
    time_delayed: 播放动画前等待多长时间（单位：毫秒）
    fadeout_speed: 淡出过程中 alpha 的变化速度
    """
    time_delayed = kwargs.pop("time_delayed", DEFAULT_TIME_DELAYED)
    fadeout_speed = kwargs.pop("fadeout_speed", DEFAULT_FADEOUT_SPEED)

    pygame.time.delay(time_delayed)

    for alpha in range(MAX_ALPHA, MIN_ALPHA, (-1) * fadeout_speed):
        screen_copy = scrmgr.screen.copy()
        screen_copy.set_alpha(alpha)

        scrmgr.clear_screen_without_update()
        scrmgr.screen.blit(screen_copy, LEFT_TOP_CORNER)

        scrmgr.update_global()

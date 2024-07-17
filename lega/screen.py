import pygame
from typing import Tuple

from pygame import Rect
from pygame.locals import FULLSCREEN

from config import color_theme, resolution

from lega.vector import Vector2D

DEFAULT_FPS = 20

class ScreenManager:
    def __init__(self, width, height):
        self._win_width = width
        self._win_height = height

        self.is_full_screen = False
        self.screen = pygame.display.set_mode(self.resolution)
        self.clock = pygame.time.Clock()
        self.fps = DEFAULT_FPS
    
    def clear_screen_without_update(self) -> None:
        self.screen.fill(color_theme.background)

    def clear_screen_with_update(self) -> None:
        """
        idiom
        """
        self.clear_screen_without_update()
        self.update_global()

    def tick(self) -> None:
        """
        control the main while loop from running too fast
        in order to reduce power consumption and generated heat
        """
        self.clock.tick(self.fps)

    def update_global(self) -> None:
        # cf. self.update_local_area()
        pygame.display.flip()

    def update_local_area(self, area: Rect) -> None:
        # cf. self.update_global()
        pygame.display.update(area)

    def toggle_fullscreen(self) -> None:
        self.is_full_screen = not self.is_full_screen
        content_backup = self.screen.copy()
        if self.is_full_screen:
            self.screen = pygame.display.set_mode(self.resolution, FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.resolution)

        # 修正屏幕切换所导致的显示问题。方法很简单，重新绘制一下原来的内容
        self.screen.fill(color_theme.background)
        self.screen.blit(content_backup, self.screen.get_rect())
        self.update_global()
    
    def toggle_resolution(self, res: tuple[int, int]) -> None:
        assert not self.is_full_screen, "暂不支持全屏模式上切换分辨率"

        self._win_width, self._win_height = res

        self.screen = pygame.display.set_mode(self.resolution)

        # 暂不解决切换分辨率之后需要重绘画面的问题
        # 假设只在进入某个游戏的时候会切换分辨率
        # 比如从 Card Prisoner 退出之后进入 Magic Tower
        ...

    @property
    def center(self) -> Vector2D:
        return Vector2D(self.win_width // 2, self.win_height // 2)

    @property
    def resolution(self) -> Tuple[int, int]:
        return self.win_width, self.win_height

    @property
    def win_height(self) -> int:
        return self._win_height

    @property
    def win_width(self) -> int:
        return self._win_width
    
    @property
    def font_size_normal(self) -> int:
        """
        * 20 for 1280x720
        * 20 for 800x600
        """
        size = self._win_height // 9 // 4
        if size < 20:
            size = 20
        return size
    
    @property
    def font_size_large(self) -> int:
        size = self.font_size_normal * 2
        return size
    
    @property
    def default_line_distance(self) -> int:
        """
        * 40 for 1280x720
        * 40 for 800x600
        """
        line_distance = self._win_height // 9 // 2
        if line_distance < 40:
            line_distance = 40
        return line_distance
    
    @property
    def default_border_thickness(self) -> int:
        return self._win_width // 16 // 40
    
    @property
    def default_border_radius(self) -> int:  # 圆角矩形相关
        return self._win_width // 16 // 4


# initialize
scrmgr = ScreenManager(resolution.INITIAL_WINDOW_WIDTH, resolution.INITIAL_WINDOW_HEIGHT)

from lega.screen import scrmgr
import lega.draw

from pygame import Surface, Rect
import pygame.draw

from config import color_theme

class TextBox:
    def __init__(self):
        width = scrmgr.win_width * 3 / 4
        height = scrmgr.win_height * 4 / 9
        self.surface = Surface((width, height))
        self.rect = self.surface.get_rect(top=0, right=scrmgr.win_width)

        padding_x = 80
        padding_top = 20
        padding_bottom = 10
        padding_y = padding_top + padding_bottom
        border_width = width- padding_x
        border_height = height - padding_y
        self.border_rect = Rect(
            # left and top are relative to local surface
            padding_x * 0.5, padding_top,
            border_width, border_height,
        )

        self._text = None
    
    def set_text(self, text):
        self._text = text

    def draw_everything(self):
        self.surface.fill(color_theme.background)

        # draw border
        pygame.draw.rect(
            self.surface,
            color_theme.foreground,
            self.border_rect,
            scrmgr.default_border_thickness,
            scrmgr.default_border_radius,
        )

        if self._text is None:
            text = ""
        else:
            text = self._text

        lega.draw.text_multi_line(self.surface, text, reference_point=self.border_rect.center)

        scrmgr.screen.blit(self.surface, self.rect)
        scrmgr.update_local_area(self.rect)

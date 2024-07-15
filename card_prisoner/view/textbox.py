from lega.draw import text_multi_line
from lega.screen import scrmgr

from pygame import Surface, Rect
import pygame.draw

from config import color_theme

from card_prisoner.shared.misc import BORDER_RADIUS

from card_prisoner.shared.misc import BORDER_THICKNESS

class TextBox:
    def __init__(self):
        self.width = scrmgr.win_width * 3 / 4
        self.height = scrmgr.win_height * 4 / 9
        self.surface = Surface((self.width, self.height))
        self.rect = self.surface.get_rect(top=0, right=scrmgr.win_width)

        padding_x = 80
        padding_top = 20
        padding_bottom = 10
        padding_y = padding_top + padding_bottom
        border_width = self.width- padding_x
        border_height = self.height - padding_y
        self.border_rect = Rect(
            # left and top are relative to local surface
            padding_x * 0.5, padding_top,
            border_width, border_height,
        )

        self.text = None
    
    def set_text(self, text):
        self.text = text

    def draw_everything(self):
        self.surface.fill(color_theme.background)

        pygame.draw.rect(self.surface, color_theme.foreground, self.border_rect, BORDER_THICKNESS, BORDER_RADIUS)

        if self.text is None:
            text = ""
        else:
            text = self.text

        text_multi_line(self.surface, text, reference_point=self.border_rect.center)

        scrmgr.screen.blit(self.surface, self.rect)
        scrmgr.update_local_area(self.rect)

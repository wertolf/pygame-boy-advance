import pygame.image
import pygame.transform
from pygame import Rect, Surface
from config import filenames, color_theme

if not pygame.image.get_extended():
    raise AssertionError("Unable to load png files.")

BOX_WIDTH = 32
BOX_HEIGHT = 32
BOX_SIZE_ORIGINAL = (BOX_WIDTH, BOX_HEIGHT)  # 图像素材的原始尺寸
BOX_SIZE_RESIZED = (64, 64)  # 放大后的尺寸

scale_func = pygame.transform.scale  # 放大图像时使用的算法

mask_rect = Rect((0, 0), BOX_SIZE_ORIGINAL)  # 用于裁剪过程中进行定位的矩形

TERRAINS = pygame.image.load(filenames.TERRAINS)

EMPTY = Surface(BOX_SIZE_RESIZED)
EMPTY.fill(color_theme.background)

ROCK = scale_func(
    TERRAINS.subsurface(mask_rect),
    BOX_SIZE_RESIZED,
)

mask_rect.y += BOX_HEIGHT

GRASS = scale_func(
    TERRAINS.subsurface(mask_rect),
    BOX_SIZE_RESIZED,
)

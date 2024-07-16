import pygame.draw
import pygame.font

from config import color_theme
from lega.calc import calculate_centery
from lega.screen import scrmgr


def text_single_line(target_surface, text, selected=False, **kwargs):
    """
    target_surface: 将文本绘制到哪里
    text: 想要绘制的**单行**文本
    selected: 是否启用被选中的效果

    bold: 是否粗体
    antialias:
    font_size: 字体大小
    color: 文字的颜色

    Specify position using kwargs.
    """

    assert "\n" not in text, "Got unexpected newline character when drawing single line text."

    bold = kwargs.pop("bold", True)
    antialias = kwargs.pop("antialias", True)
    default_font_size = scrmgr.font_size_normal
    font_size = kwargs.pop("font_size", default_font_size)
    color = kwargs.pop("color", color_theme.foreground)

    font_object = pygame.font.SysFont("Courier New", font_size, bold)
    text_surface = font_object.render(text, antialias, color)
    text_rect = text_surface.get_rect(**kwargs)

    target_surface.blit(text_surface, text_rect)

    if selected:
        # 在文本左右两侧绘制圆圈
        radius = font_size / 4
        distance = font_size
        center = (
            text_rect.left - distance,
            text_rect.centery
        )
        pygame.draw.circle(target_surface, color, center, radius)
        center = (
            text_rect.right + distance,
            text_rect.centery
        )
        pygame.draw.circle(target_surface, color, center, radius)


def text_multi_line(target_surface, text, reference_point, reference_type="center", **kwargs):
    """
    reference_point: 参照点的坐标
    reference_type: 参照点的类型，目前只支持居中对齐 (center)
    line_distance: 行间距
    """
    default_line_distance = scrmgr.default_line_distance
    line_distance = kwargs.pop("line_distance", default_line_distance)
    lines = text.split("\n")

    reference_x = reference_point[0]
    reference_y = reference_point[1]

    if reference_type != "center":
        raise AssertionError(f"Got unexpected reference type: {reference_type}")
    else:
        n_lines = len(lines)
        reference_y = calculate_centery(n_lines, reference_y, line_distance)

    for line in lines:
        text_single_line(target_surface, line, centerx=reference_x, centery=reference_y, **kwargs)
        reference_y += line_distance
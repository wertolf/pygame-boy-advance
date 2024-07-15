from card_prisoner.view.view import View
from card_prisoner.model.player import Player

from lega.screen import scrmgr

from lega.an import global_fadeout

import lega.draw

def victory_animation():
    """
    胜利动画
    """

    global_fadeout()

    lega.draw.text_single_line(
        scrmgr.screen, "YOU WON (PRESS R TO RESTART)",
        centerx=scrmgr.center.x, centery=scrmgr.center.y
    )

    scrmgr.update_global()


def game_over_animation():
    """
    失败动画
    """

    global_fadeout()

    lega.draw.text_multi_line(
        scrmgr.screen,
        "GAME OVER\n"
        "(PRESS R TO RESTART)",
        reference_point=scrmgr.center,
    )

    scrmgr.update_global()

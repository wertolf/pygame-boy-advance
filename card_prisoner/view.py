"""
视图相关的最大单位/对象

与子对象构成 composite 的关系
"""

from enum import Enum
from card_prisoner.sidebar import SideBar, SideBarOptions
from card_prisoner.item_list import ItemList, ItemListMode, InventoryItemIndex, ShopItemIndex
from card_prisoner.textbox import TextBox

from card_prisoner import messages


class ViewMode(Enum):
    LEVEL_1 = 1  # 可以操作 1 级列表
    LEVEL_2 = 2  # 可以操作 2 级列表


class View:
    def __init__(self):
        self.sidebar = SideBar()
        self.item_list = ItemList()
        self.textbox = TextBox()

        # initialization is a little different than setters
        # in order to avoid some bug
        # such as unexpected help message on start up
        self._mode = ViewMode.LEVEL_1
        self.sidebar.is_activated = True
        self.item_list.is_activated = False

    @property
    def mode(self):
        return self._mode
    
    @mode.setter
    def mode(self, value):
        self._mode = value
        match self._mode:
            case ViewMode.LEVEL_1:
                self.sidebar.is_activated = True
                self.item_list.is_activated = False

            case ViewMode.LEVEL_2:
                self.sidebar.is_activated = False
                self.item_list.is_activated = True

            case _:
                raise AssertionError(f"Got unexpected mode: {self._mode}")

    def draw_everything(self):
        self.sidebar.draw_everything()
        self.textbox.draw_everything()
        self.item_list.draw_everything()

        # 由于 view 的各组件的 draw_everything 方法在末尾分别更新了各自的局部
        # 因此这里不需要在调用 scrmgr.update_global

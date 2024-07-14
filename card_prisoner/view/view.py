"""
视图相关的最大单位/对象

与子对象构成 composite 的关系
"""

from enum import Enum
from card_prisoner.view.sidebar import SideBar, SideBarOptions
from card_prisoner.view.item_list import ItemList, ItemListMode, InventoryItemIndex, ShopItemIndex, SkillItemIndex
from card_prisoner.view.textbox import TextBox

from card_prisoner.shared import messages


class ViewMode(Enum):
    LEVEL_1 = 1  # 可以操作 1 级列表
    LEVEL_2 = 2  # 可以操作 2 级列表


class View:
    def __init__(self):
        self._initialized = False

        self.sidebar = SideBar()
        self.item_list = ItemList()
        self.textbox = TextBox()
        self.textbox.set_text(messages.ABOUT)

        # initialization is a little different than setters
        # in order to avoid some bug
        # such as unexpected help message on start up
        self._mode = ViewMode.LEVEL_1
        self.sidebar.is_activated = True
        self.item_list.is_activated = False
        self._sidebar_option_index = 0
        self._item_list_index = 0

        self._initialized = True

        self.global_update_needed = True
    
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

        self.update_default_message()

        self.global_update_needed = True

    def draw_everything(self, player):
        self.sidebar.draw_everything(player, selected_index=self.sidebar_option_index)
        self.textbox.draw_everything()
        self.item_list.draw_everything(player, selected_index=self.item_list_index)

    @property
    def sidebar_option_index(self):
        return self._sidebar_option_index
    
    @sidebar_option_index.setter
    def sidebar_option_index(self, value):
        if value < 0 or value > len(self.sidebar.options) - 1:
            return
        
        assert self.mode == ViewMode.LEVEL_1, f"Unexpected action change in mode {self.mode}"

        self._sidebar_option_index = value

        option = self.sidebar.options[self._sidebar_option_index]
        match option:
            case SideBarOptions.INVENTORY:
                self.item_list.mode = ItemListMode.INVENTORY
            case SideBarOptions.SHOP:
                self.item_list.mode = ItemListMode.SHOP
            case SideBarOptions.SKILLS:
                self.item_list.mode = ItemListMode.SKILLS
            case _:
                self.item_list.mode = ItemListMode.EMPTY

        self.update_default_message()

        self.global_update_needed = True
    
    @property
    def item_list_index(self):
        return self._item_list_index
    
    @item_list_index.setter
    def item_list_index(self, value):
        if value < 0 or value > self.item_list.n_rows * self.item_list.n_cols - 1:
            return

        assert self.mode == ViewMode.LEVEL_2, f"Unexpected inventory item change in mode {self.mode}"

        self._item_list_index = value

        self.update_default_message()

        self.global_update_needed = True

    def update_default_message(self):
        """
        根据当前选项决定显示的帮助信息

        NOTE:
        如果想要给 self.textbox 设定自定义信息，
        直接调用 self.textbox.set_text 然后将 self.global_update_needed 设置为 True 即可
        """
        text = (
            "This is a default message.\n"
            "To change it, modify View.update_message()."
        )
        option = self.sidebar.options[self._sidebar_option_index]
        if self.mode is ViewMode.LEVEL_1:
            match option:
                case SideBarOptions.BACK:
                    text = messages.BACK
                case SideBarOptions.END_TODAY:
                    text = messages.END_TODAY
                case SideBarOptions.INVENTORY:
                    text = messages.INVENTORY
                case SideBarOptions.SHOP:
                    text = messages.SHOP
                case SideBarOptions.SKILLS:
                    text = messages.SKILLS
                case SideBarOptions.ABOUT:
                    text = messages.ABOUT
        elif self.mode is ViewMode.LEVEL_2:
            match self.item_list.mode:
                case ItemListMode.INVENTORY:
                    match self._item_list_index:
                        case InventoryItemIndex.SSR:
                            text = messages.SSR
                        case InventoryItemIndex.FOOD:
                            text = messages.FOOD
                        case InventoryItemIndex.WATER:
                            text = messages.WATER
                        case InventoryItemIndex.ASPIRIN:
                            text = messages.ASPIRIN
                        case _:
                            text = messages.EXIT
                case ItemListMode.SHOP:
                    match self._item_list_index:
                        case ShopItemIndex.DRAW_1_CARD:
                            text = messages.DRAW_1_CARD
                        case ShopItemIndex.DRAW_5_CARDS:
                            text = messages.DRAW_5_CARDS
                        case ShopItemIndex.DRAW_10_CARDS:
                            text = messages.DRAW_10_CARDS
                        case _:
                            text = messages.EXIT
                case ItemListMode.SKILLS:
                    match self._item_list_index:
                        case SkillItemIndex.HUNGER_RESISTANCE:
                            text = messages.HUNGER_RESISTANCE
                        case SkillItemIndex.THIRST_RESISTANCE:
                            text = messages.THIRST_RESISTANCE
                        case _:
                            text = messages.EXIT

        self.textbox.set_text(text)
        self.global_update_needed = True

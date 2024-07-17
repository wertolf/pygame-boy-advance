from enum import Enum

# Cards

SSR = "SSR Card"
A = "A-class Card"
B = "B-class Card"
C = "C-class Card"
FOOD = "Food Card"
WATER = "Water Card"

SUPPLY = (FOOD, WATER)

CARD_DICT = {
    SSR: {
        "abbr": "SSR",
        "desc": (
            "Very very rare card.\n"
            "Get 10 of this card to win the game!"
        ),
    },
    A: {
        "abbr": "A",
        "desc": (
            "Normal card. Can be used to exchange items in shop.\n"
        ),
    },
    B: {
        "abbr": "B",
        "desc": (
            "Normal card. Can be used to exchange items in shop.\n"
        ),
    },
    C: {
        "abbr": "C",
        "desc": (
            "Normal card. Can be used to exchange items in shop.\n"
        ),
    },
    FOOD: {
        "abbr": "Food",
        "desc": (
            "This card gives you some food."
        ),
    },
    WATER: {
        "abbr": "Water",
        "desc": (
            "This card gives you some water."
        ),
    },

}

# Talents (special skills)

MONEY_MAKER = "Money Maker"
SHOP_BARGAINER = "Shop Bargainer"
LUCKY_MAN = "Lucky Man"

TALENT_DICT = {
    MONEY_MAKER: {
        "abbr": "$++",
        "desc": (
            "Earn more money every day."
        ),
    },
    SHOP_BARGAINER: {
        "abbr": "BGN",
        "desc": (
            "Buy things at shop with lower prices."
        ),
    },
    LUCKY_MAN: {
        "abbr": "LKY",
        "desc": (
            "More likely to get SSR cards."
        ),
    },
}

# Skills

HUNGER_RESIST = "Hunger Resistance"
THIRST_RESIST = "Thirst Resistance"

SKILL_DICT = {
    HUNGER_RESIST: {
        "abbr": "HGR--",
        "desc": (
            "Reduce HP decrease per day."
        ),
    },
    THIRST_RESIST: {
        "abbr": "TST--",
        "desc": (
            "Reduce MP decrease per day."
        ),
    },
}

# combine the above dicts together
EMPTY_ITEM = ""
ITEM_DICT = {
    EMPTY_ITEM: {
        "abbr": "",
        "desc": (
            "This slot is empty.\n"
            "Press X to exit."
        ),
    },
}
ITEM_DICT.update(CARD_DICT)
ITEM_DICT.update(SKILL_DICT)
ITEM_DICT.update(TALENT_DICT)

class Item:
    def __init__(self, item_name: str = EMPTY_ITEM):
        self.item_name = item_name
        self.abbr = ITEM_DICT[self.item_name]["abbr"]
    def __str__(self):
        """
        绘制 ItemList 的时候要用到
        可以被子类重写
        """
        return self.abbr


class InventoryItem(Item):
    def __init__(self, item_name: str, quantity: int):
        super().__init__(item_name)
        self.quantity = quantity
    
    def __str__(self):
        return (
            "\n"
            f"{self.abbr}\n"
            f"x{self.quantity}"
        )
        

class ShopItemStatus(Enum):
    ON_SALE = 1  # 在售：我可以买的东西
    # TODO: 我要卖的东西应该称作什么

class ShopItem(InventoryItem):
    def __init__(self, item_name: str, quantity: int, price: InventoryItem, status: ShopItemStatus):
        super().__init__(item_name, quantity)
        self.price = price
        self.status = status


class SkillItem(Item):
    def __init__(self, item_name: str, level: int):
        super().__init__(item_name)

        self.level = level
    def __str__(self):
        return (
            "\n"
            f"{self.abbr}\n"
            f"Lv {self.level}"
        )


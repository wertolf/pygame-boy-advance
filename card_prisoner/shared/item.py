from enum import Enum

class Item:
    def __init__(self, item, quantity: int):
        self.item = item
        self.quantity = quantity

class ShopItemStatus(Enum):
    ON_SALE = 1  # 在售：我可以买的东西
    # TODO: 我要卖的东西应该称作什么

class ShopItem(Item):
    def __init__(self, item, quantity, price: Item, status: ShopItemStatus):
        super().__init__(item, quantity)
        self.price = price
        self.status = status

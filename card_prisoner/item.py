from enum import Enum

class Item:
    def __init__(self, item_name: str):
        self.item_name = item_name
    def __str__(self):
        """
        绘制 ItemList 的时候要用到
        可以被子类重写
        """
        return self.item_name


class InventoryItem(Item):
    def __init__(self, item_name: str, quantity: int):
        super().__init__(item_name)
        self.quantity = quantity
    
    def __str__(self):
        return (
            "\n"
            f"{self.item_name}\n"
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


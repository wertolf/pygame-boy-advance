from card_prisoner.item import OnSaleItem, WantedItem, SUPPLY, ORDINARY
from card_prisoner.item import InventoryItem
import random

N_ON_SALE_ITEMS_PER_DAY = 3

N_WANTED_ITEMS_PER_DAY = 1

class Shop:
    def __init__(self, price_is_lower):
        self.on_sale_items = []
        self.wanted_items = []

        # Shop Bargainer 的技能
        self.price_is_lower = price_is_lower

        self.refresh_items()

    def refresh_items(self):

        self.on_sale_items.clear()
        for _ in range(N_ON_SALE_ITEMS_PER_DAY):
            card_name = random.choice(SUPPLY)
            quantity = random.randint(1, 3)

            # 用来交换的卡片类型及所需数量
            exchange_card_name = random.choice(ORDINARY)
            exchange_card_quantity = random.randint(2, 4)
            price = InventoryItem(exchange_card_name, exchange_card_quantity)

            # Shop Bargainer 的技能
            if self.price_is_lower:
                price.quantity //= 2

            item = OnSaleItem(card_name, quantity, price)
            self.on_sale_items.append(item)

        self.wanted_items.clear()
        for _ in range(N_WANTED_ITEMS_PER_DAY):
            card_name = random.choice(SUPPLY)
            price = random.randint(30, 50)

            item = WantedItem(card_name, price)
            self.wanted_items.append(item)

from card_prisoner.item import Item

from enum import Enum

class SkillItem(Item):
    def __init__(self, item_name: str, level: int):
        super().__init__(item_name)

        self.level = level
    def __str__(self):
        return (
            "\n"
            f"{self.item_name}\n"
            f"Lv {self.level}"
        )

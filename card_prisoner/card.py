from enum import Enum

class CardNames(Enum):
    SSR = "SSR"
    A = "A"
    B = "B"
    C = "C"
    FOOD = "Food"
    WATER = "Water"

SUPPLY = (CardNames.FOOD, CardNames.WATER)

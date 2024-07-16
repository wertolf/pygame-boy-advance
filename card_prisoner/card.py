from enum import Enum

class CardNames(Enum):
    SSR = "SSR"
    A = "A"
    B = "B"
    C = "C"
    FOOD = "Food"
    WATER = "Water"
    ASPIRIN = "Aspirin"
    VITAMIN = "Vitamin"
    TRANQUILIZER = "Tranquilizer"

MEDICINE = (CardNames.ASPIRIN, CardNames.VITAMIN, CardNames.TRANQUILIZER)
SUPPLY = MEDICINE + (CardNames.FOOD, CardNames.WATER)

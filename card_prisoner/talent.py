from enum import Enum
import random

N_TALENTS = 2  # 玩家所拥有的天赋数量

class TalentNames(str, Enum):
    MONEY_MAKER = "$MKR"
    BARGAIN = "BGN"
    LUCKY_MAN = "LKY"

TALENT_DESC = {
    TalentNames.MONEY_MAKER:
        "Earn more money every day.",
    TalentNames.BARGAIN:
        "Buy things in shop at lower prices.",
    TalentNames.LUCKY_MAN:
        "More likely to get SSR cards.",
}

TALENT_POOL = [talent for talent in TalentNames]

def get_random_talent():
    i = random.randint(0, len(TALENT_POOL) - 1)
    return TALENT_POOL[i]

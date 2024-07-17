import random

N_TALENTS = 2  # 玩家所拥有的天赋数量

# talent names (abbreviations)
MONEY_MAKER = "$MKR"
BARGAIN = "BGN"
LUCKY_MAN = "LKY"

TALENT_POOL = [
    MONEY_MAKER,
    BARGAIN,
    LUCKY_MAN,
]

TALENT_DESC = {
    MONEY_MAKER:
        "Earn more money every day.",
    BARGAIN:
        "Buy things in shop at lower prices.",
    LUCKY_MAN:
        "More likely to get SSR cards.",
}

def get_random_talent():
    i = random.randint(0, len(TALENT_POOL) - 1)
    return TALENT_POOL[i]

from enum import Enum
import random

N_TALENTS = 2  # 玩家所拥有的天赋数量

class TalentNames(Enum):
    # value 对应希望的文本显示
    MONEY_MAKER = "Money\nMaker"  # 每日收入增加
    BARGAINER = "Bar-\ngainer"  # 购买商品时价格降低
    LUCKYMAN = "Lucky\nMan"  # 抽到 SSR 的概率增加

TALENT_POOL = [talent for talent in TalentNames]

def get_random_talent():
    i = random.randint(0, len(TALENT_POOL) - 1)
    return TALENT_POOL[i]

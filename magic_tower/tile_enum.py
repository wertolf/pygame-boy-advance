from enum import Enum

class TileEnum(Enum):
    VOID = "V"  # 虚空，等于星辰
    STAR = "V"  # 星辰
    GROUND = "G"  # 普通地面，为简化设计，等于草地
    GRASS = "G"  # 草地
    WALL = "W"  # 墙壁
    LAVA = "L"  # 岩浆
    UPSTAIR = "U"  # 向上的楼梯
    DOWNSTAIR = "D"  # 向下的楼梯

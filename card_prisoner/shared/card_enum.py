from enum import Flag

class CardEnum(Flag):
    SSR = 1
    SR = 2
    R = 4
    A = 8
    B = 16
    C = 32
    FOOD = 64
    WATER = 128
    ASPIRIN = 256
    VITAMIN = 512
    TRANQUILIZER = 1024
    MED = ASPIRIN | VITAMIN | TRANQUILIZER
    SUPPLY = FOOD | WATER | MED

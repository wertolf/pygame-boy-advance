from card_prisoner import messages
from card_prisoner.item import TalentItem
from card_prisoner.item import InventoryItem, TALENT_DICT, MONEY_MAKER, LUCKY_MAN
from card_prisoner.item import (
    SSR,
    A,
    B,
    C,
    FOOD,
    WATER,
)

import logging
import random

class Player:
    def __init__(self):
        self._HP = 100
        self._MP = 100

        self.age = 1  # number of elapsed days (in game)
        self.money = 100
        self.inventory = {
            SSR: InventoryItem(SSR, 0),
            A: InventoryItem(A, 0),
            B: InventoryItem(B, 0),
            C: InventoryItem(C, 0),
            FOOD: InventoryItem(FOOD, 0),
            WATER: InventoryItem(WATER, 0),
        }

        N_TALENTS = 2  # 玩家所拥有的天赋数量
        TALENT_POOL = list(TALENT_DICT.keys())
        self.talents = []
        for _ in range(N_TALENTS):
            # TODO: duplicate code
            i = random.randint(0, len(TALENT_POOL) - 1)
            talent = TALENT_POOL[i]
            while talent in self.talents:  # retry if already has this talent
                # TODO: duplicate code
                i = random.randint(0, len(TALENT_POOL) - 1)
                talent = TALENT_POOL[i]
            self.talents.append(talent)
        self.talents = [
            TalentItem(talent, level="max")  # level=max 是因为天赋无法升级
            for talent in self.talents
        ]

        self.death_reason = None
    
    def eat_food(self):
        if self.inventory[FOOD].quantity > 0:
            self.inventory[FOOD].quantity -= 1
            self.HP += self.HP_increase_per_food_card
            
    def drink_water(self):
        if self.inventory[WATER].quantity > 0:
            self.inventory[WATER].quantity -= 1
            self.MP += self.MP_increase_per_water_card

    def sleep(self):
        self.age += 1

        self.HP -= self.HP_decrease_per_day
        self.MP -= self.MP_decrease_per_day 

        self.money += self.money_earned_per_day

    @property
    def HP(self):
        return self._HP
    
    @HP.setter
    def HP(self, value):
        if value < 0:
            value = 0
        elif value > 100:
            value = 100
        self._HP = value

    @property
    def MP(self):
        return self._MP
    
    @MP.setter
    def MP(self, value):
        if value < 0:
            value = 0
        elif value > 100:
            value = 100
        self._MP = value

    def is_dead(self):
        if self.HP == 0:
            self.death_reason = messages.GAME_OVER_HUNGER
            return True
        elif self.MP == 0:
            self.death_reason = messages.GAME_OVER_THIRST
            return True
        
        return False
    
    def has_won(self):
        return self.inventory[SSR].quantity >= 10
    
    def is_game_over(self):
        return self.is_dead() or self.has_won()

    @property
    def HP_decrease_per_day(self):
        value = 20

        # TODO: HUNGER_RESIST

        return value
    
    @property
    def MP_decrease_per_day(self):
        value = 20

        # TODO: THIRST RESIST

        return value

    @property
    def money_earned_per_day(self):
        value = 50

        if MONEY_MAKER in [talent.item_name for talent in self.talents]:
            value *= 2

        return value

    @property
    def HP_increase_per_food_card(self):
        return 20

    @property
    def MP_increase_per_water_card(self):
        return 20

    @property
    def SSR_probability(self):
        """
        抽到 SSR 卡的概率
        """
        value = 0.01

        if LUCKY_MAN in [talent.item_name for talent in self.talents]:
            value *= 2
        
        return value

    @property
    def SUPPLY_probability(self):
        """
        抽到补给类卡的概率
        """
        value = 0.1

        if LUCKY_MAN in [talent.item_name for talent in self.talents]:
            value *= 2
        
        return value

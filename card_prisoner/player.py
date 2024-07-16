from card_prisoner import messages
from card_prisoner.skill import SkillItem
from card_prisoner.card import CardNames
from card_prisoner.item import InventoryItem
from card_prisoner.talent import N_TALENTS, get_random_talent

import logging

class Player:
    def __init__(self):
        self._HP = 100
        self._MP = 100

        self.age = 1  # number of elapsed days (in game)
        self.money = 100
        self.inventory = {
            CardNames.SSR: InventoryItem(CardNames.SSR.value, 0),
            CardNames.A: InventoryItem(CardNames.A.value, 0),
            CardNames.B: InventoryItem(CardNames.B.value, 0),
            CardNames.C: InventoryItem(CardNames.C.value, 0),

            CardNames.FOOD: InventoryItem(CardNames.FOOD.value, 0),
            CardNames.WATER: InventoryItem(CardNames.WATER.value, 0),

            CardNames.ASPIRIN: InventoryItem(CardNames.ASPIRIN.value, 0),
        }

        self.talents = []
        for i in range(N_TALENTS):
            talent = get_random_talent()
            while talent in self.talents:  # retry if already has this talent
                talent = get_random_talent()
            self.talents.append(talent)
        # level=1 是因为天赋只有 1 级
        self.talents = [SkillItem(talent.value, level=1) for talent in self.talents]

        self.death_reason = None
    
    def eat_food(self):
        if self.inventory[CardNames.FOOD].quantity > 0:
            self.inventory[CardNames.FOOD].quantity -= 1
            self.HP += self.HP_increase_per_food_card
            
    def drink_water(self):
        if self.inventory[CardNames.WATER].quantity > 0:
            self.inventory[CardNames.WATER].quantity -= 1
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
        return self.inventory[CardNames.SSR].quantity >= 10
    
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

        # TODO: DEFINE & IMPLEMENT A SKILL

        return value

    @property
    def HP_increase_per_food_card(self):
        return 20

    @property
    def MP_increase_per_water_card(self):
        return 20

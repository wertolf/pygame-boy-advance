from card_prisoner.shared import messages
from card_prisoner.shared.card_enum import CardEnum
from card_prisoner.shared.item import Item

import logging

from enum import Enum

class PlayerStatus(Enum):
    NORMAL = "Normal"
    FEVER = "Fever"

class Player:
    def __init__(self):
        self._health = 100
        self._thirst = 100
        self._sanity = 100

        self.age = 1  # number of elapsed days (in game)
        self.status = PlayerStatus.NORMAL
        self.money = 100
        self.token = 0  # “命运之尘”代币
        self.inventory = {
            CardEnum.SSR: Item(CardEnum.SSR, 0),
            CardEnum.A: Item(CardEnum.A, 0),
            CardEnum.B: Item(CardEnum.B, 0),
            CardEnum.C: Item(CardEnum.C, 0),

            CardEnum.FOOD: Item(CardEnum.FOOD, 0),
            CardEnum.WATER: Item(CardEnum.WATER, 0),

            CardEnum.ASPIRIN: Item(CardEnum.ASPIRIN, 0),
        }

        self.death_reason = None
    
    def eat_food(self):
        if self.inventory[CardEnum.FOOD].quantity > 0:
            self.inventory[CardEnum.FOOD].quantity -= 1
            self.health += self.health_increase_per_food_card
            
            logging.critical(f"You ate some food. Health = {self.health}.")
    
    def drink_water(self):
        if self.inventory[CardEnum.WATER].quantity > 0:
            self.inventory[CardEnum.WATER].quantity -= 1
            self.thirst += self.thirst_increase_per_water_card

            logging.critical(f"You drank some water. Thirst = {self.thirst}.")

    def sleep(self):
        self.age += 1

        self.health -= self.health_decrease_per_day
        self.thirst -= self.thirst_decrease_per_day 

        self.money += self.money_earned_per_day

    @property
    def health(self):
        return self._health
    
    @health.setter
    def health(self, value):
        if value < 0:
            value = 0
        elif value > 100:
            value = 100
        self._health = value

    @property
    def thirst(self):
        return self._thirst
    
    @thirst.setter
    def thirst(self, value):
        if value < 0:
            value = 0
        elif value > 100:
            value = 100
        self._thirst = value

    @property
    def sanity(self):
        return self._sanity
    
    @sanity.setter
    def sanity(self, value):
        if value < 0:
            value = 0
        elif value > 100:
            value = 100
        self._sanity = value

    def is_dead(self):
        if self.health == 0:
            self.death_reason = messages.GAME_OVER_HUNGER
            return True
        elif self.thirst == 0:
            self.death_reason = messages.GAME_OVER_THIRST
            return True
        
        return False
    
    def has_won(self):
        return self.inventory[CardEnum.SSR].quantity >= 10
    
    def is_game_over(self):
        return self.is_dead() or self.has_won()

    @property
    def health_decrease_per_day(self):
        value = 20

        # TODO: HUNGER_RESIST

        return value
    
    @property
    def thirst_decrease_per_day(self):
        value = 20

        # TODO: THIRST RESIST

        return value

    @property
    def money_earned_per_day(self):
        value = 50

        # TODO: DEFINE & IMPLEMENT A SKILL

        return value

    @property
    def health_increase_per_food_card(self):
        return 20

    @property
    def thirst_increase_per_water_card(self):
        return 20

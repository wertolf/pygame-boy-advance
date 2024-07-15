from card_prisoner.model.player import Player
from card_prisoner.view.view import View
from card_prisoner.shared.card_enum import CardEnum
from card_prisoner.shared.misc import PRICE_PER_CARD, SANITY_INCREASE_AFTER_GOT_SSR

import random

def cheat(view: View, player: Player):
    player.inventory[CardEnum.FOOD].quantity += 5
    player.inventory[CardEnum.WATER].quantity += 5

    view.textbox.set_text(
        "You pressed the cheat key.\n"
        "Got 5 food card.\n"
        "Got 5 water card."
    )

def eat_food(view: View, player: Player):
    # update model
    player.eat_food()

    # update view
    # here we can give textbox some text

def drink_water(view: View, player: Player):
    # update model
    player.drink_water()

    # update view
    # here we can give textbox some text

def draw_card(view: View, player: Player):
    if player.money >= PRICE_PER_CARD:

        player.money -= PRICE_PER_CARD

        number = random.random()
        if number < 0.01:  # TODO: hard-coded value
            card = CardEnum.SSR
        elif number < 0.05:
            card = CardEnum.FOOD
        elif number < 0.1:
            card = CardEnum.WATER
        elif number < 0.3:  # TODO: hard-coded value
            card = CardEnum.A
        elif number < 0.6:  # TODO: hard-coded value
            card = CardEnum.B
        else:
            card = CardEnum.C

        player.inventory[card].quantity += 1

        text = "Got %s card." % card.name

        if card == CardEnum.SSR:
            player.sanity += SANITY_INCREASE_AFTER_GOT_SSR
            text = "GOT SSR CARD!!!"
        elif card not in CardEnum.SUPPLY:
            sanity_decrease = random.randint(1, 5)
            player.sanity -= sanity_decrease
            text += "\nSanity -= %d" % sanity_decrease

        view.textbox.set_text(text)

    else:  # player.money < PRICE_PER_CARD
        view.textbox.set_text(
            "You do not have enough money!",
        )

def end_today(view: View, player: Player):

    # update model

    player.sleep()

    # update view

    view.sidebar_option_index = view.sidebar_option_index  # call action_index.setter to update inventory properly

    msg = (
        f"*** Day {player.age:02d} ***\n"
        f"Health -= {player.health_decrease_per_day}\n"
        f"Thirst -= {player.thirst_decrease_per_day}\n"
    )

    view.textbox.set_text(msg)

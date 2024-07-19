import pygame.key
from config import key_bindings

# 帮助信息/指导语 (instructions)

ABOUT = (
    "Welcome!\n"
    "Use arrow keys to navigate.\n"
    f"Press {pygame.key.name(key_bindings.CONFIRM)} to confirm"
        f", {pygame.key.name(key_bindings.CANCEL)} to cancel.\n"
    f"Press {pygame.key.name(key_bindings.DRAW_CARD)} to draw card.\n"
    f"Press {pygame.key.name(key_bindings.DISPLAY_HELP)} to display help.\n"
    "Get 10 SSR cards to win!"
)

END_TODAY = "Sleep and go to the next day."

INVENTORY = f"Press {pygame.key.name(key_bindings.CONFIRM)} to view and use cards."

SHOP = f"Press {pygame.key.name(key_bindings.CONFIRM)} to view and buy shop items."

TALENT = f"Press {pygame.key.name(key_bindings.CONFIRM)} to view your talents."

# save/load

SAVE_SUCCESS = "Game saved."
LOAD_SUCCESS = "Game loaded."
LOAD_NOT_FOUND = (
    "You do not have a save file.\n"
    f"To create one, press the {pygame.key.name(key_bindings.SAVE_GAME)} key."
)

# help

HELP = [
    # start of new page
    "*** Basic Key Binding ***\n"
    "\n"
    "Use arrow keys to navigate.\n"
    f"Press {pygame.key.name(key_bindings.CONFIRM)} to confirm"
        f", {pygame.key.name(key_bindings.CANCEL)} to cancel.\n"
    f"Press {pygame.key.name(key_bindings.DRAW_CARD)} to draw card.\n"
    f"Press {pygame.key.name(key_bindings.DISPLAY_HELP)} to display help.\n"
    f"Press {pygame.key.name(key_bindings.RETURN_TO_TITLE)} to return to title.\n"
    ,

    # start of new page
    "*** More Key Bindings ***\n"
    "\n"
    f"Press {pygame.key.name(key_bindings.CHEAT)} to cheat.\n"
    f"Press {pygame.key.name(key_bindings.SAVE_GAME)} to save game progress on disk.\n"
    f"Press {pygame.key.name(key_bindings.LOAD_GAME)} to load a previously saved game.\n"
    f"Press {pygame.key.name(key_bindings.PRINT_SCREEN)} to take a screenshot.\n"
    ,

    # start of new page
    # background story (maybe ask GPT to write one)
]

# game over

GAME_OVER_HUNGER = (
    "YOU DIED OF HUNGER"
)

GAME_OVER_THIRST = (
    "YOU DIED OF THIRST"
)

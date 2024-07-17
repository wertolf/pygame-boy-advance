from card_prisoner.controller import GameController

def main():
    restart_game = True
    while restart_game:
        game = GameController()
        game.initialize_game()
        restart_game = game.start_game()


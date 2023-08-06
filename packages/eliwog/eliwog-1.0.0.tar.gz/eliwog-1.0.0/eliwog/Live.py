from GameManager import game_manager

new_game_manager = game_manager()

def load_game():
  new_game_manager.show_main_menu()

def welcome(name):
    return new_game_manager.welcome(name)
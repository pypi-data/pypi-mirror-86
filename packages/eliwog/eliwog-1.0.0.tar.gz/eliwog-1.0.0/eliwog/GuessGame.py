from Game import game


class guess_game(game):
  def __init__(self, override_menu=''):
      self.override_menu = override_menu

  def play(self, difficulty):
    self.difficulty = difficulty
    self.secret_number = self.generate_number(last_number= difficulty)
    return self.compare_results(master_number= self.secret_number, val_from_value= 1, val_to_value= difficulty)

  def get_menu(self):
      if self.override_menu:
        return self.override_menu
      else:
        return "Guess Game - guess a number and see if you chose like the computer."

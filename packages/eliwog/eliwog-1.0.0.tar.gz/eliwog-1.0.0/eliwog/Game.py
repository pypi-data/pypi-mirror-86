from abc import ABC, abstractmethod
from Common import common
from random import *

class game(ABC, common):
  def __init__(self, override_menu):
    self.difficulty = 1
    self.override_menu = override_menu

  @abstractmethod
  def play(self, difficulty):
    pass

  @abstractmethod
  def get_menu(self):
    pass

  def generate_number(self, last_number):
    if self.difficulty == 1:
      return 1
    else:
      return randint(1, last_number)

  def get_guess_from_user(self, val_from_value, val_to_value):
    return self.start_validate_input(f'Please guess a number between {val_from_value} and {val_to_value}:', val_from_value = val_from_value, val_to_value = val_to_value)

  def compare_results(self,master_number, val_from_value, val_to_value):
    return (master_number == self.get_guess_from_user(val_from_value= val_from_value, val_to_value= val_to_value))

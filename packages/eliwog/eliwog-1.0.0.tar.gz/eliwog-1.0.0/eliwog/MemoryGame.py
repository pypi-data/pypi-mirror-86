from random import *
from Game import game
from abc import ABC, abstractmethod
import time

class memory_game(game):
  def __init__(self, override_menu=''):
      self.override_menu = override_menu

  def play(self, difficulty):
    self.difficulty = difficulty
    return self._is_list_equal(game_list = self._generate_sequence(), user_list = self._get_list_from_user())

  def get_menu(self):
      if self.override_menu:
        return self.override_menu
      else:
        return "Memory Game - a sequence of numbers will appear for 1 second and you have to guess it back."

  def _generate_sequence(self):
    secret_number = []
    for index in range(self.difficulty):
      secret_number.append(randrange(1, 101))

    print(secret_number)
    time.sleep(0.7)
    self.clean_screen()
    return secret_number

  def _get_list_from_user(self):
    user_enter_numbers = False
    user_number_list = []
    print('\n\nPlease try to guess the numbers.')
    while not user_enter_numbers:
      print('Please enter a number: ')
      user_number_list.append(self.get_int_value())
      if len(user_number_list) == self.difficulty:
        user_enter_numbers = True

    return user_number_list

  def _is_list_equal(self, game_list, user_list):
    list_equal = True
    for number in game_list:
      if user_list.count(number) <= 0:
        list_equal = False
        break

    return list_equal





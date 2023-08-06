from Game import game
from exchangeratesapi import Api


class Currency_Roulette_Game(game):
  def __init__(self, override_menu=''):
      self.override_menu = override_menu


  def play(self, difficulty):
      self.difficulty = difficulty
      from_int, to_int = self._get_money_interval()
      return self._compare_results(master_number= self._get_guess_from_user(), val_from_value= from_int, val_to_value= to_int)

  def get_menu(self):
      if self.override_menu:
        return self.override_menu
      else:
        return "Currency Roulette - try and guess the value of a random amount of USD in ILS."

  def _get_rate(self):
     api = Api()
     return  api.get_rate('USD', 'ILS')

  def _get_money_interval(self):
      t = (self._get_rate() * self.generate_number(last_number = 100))
      d = self.difficulty
      return (t - (5 - d), t +  (5 - d))

  def _get_guess_from_user(self):
      print('Please guess what will be the generated number from USD to ILS:')
      return self.get_int_or_float_value()

  def _compare_results(self,master_number, val_from_value, val_to_value):
    return self.is_corret_value(input_num= master_number, from_value= val_from_value, to_value= val_to_value)
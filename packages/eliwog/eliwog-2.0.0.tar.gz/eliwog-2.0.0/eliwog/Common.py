import os

class common():

  def get_int_value(self):
    while True:
      value = input()
      if str(value).isdigit():
        return int(value)
      else:
        print('Please enter only numeric values!')

  def get_int_or_float_value(self):
    while True:
      value = input()
      if type(value == float):
        try:
          return float(value)  # in case user will type "33.4333fseffdd"
        except:
          print('Please enter only numeric')
      elif type(value == int):
        return int(value)
      else:
        print('Please enter only numeric')

  def is_corret_value(self, input_num, from_value, to_value):
    if (input_num >= from_value) and (input_num <= to_value):
      return True
    else:
      return False

  def is_big_value(self, input_num, to_value):
    if (input_num > to_value):
      return True

  def start_validate_input(self, message, val_from_value, val_to_value):
    print(message)
    answer_correct = False
    while not answer_correct:
      user_input_number = self.get_int_value()
      if self.is_corret_value(input_num=user_input_number, from_value=val_from_value, to_value=val_to_value):
        answer_correct = True
      else:
        if self.is_big_value(input_num=user_input_number, to_value=val_to_value):
          print(f'{user_input_number} is too big, ' + message)
        else:
          print(f'{user_input_number} is too small, ' + message)

    return user_input_number

  def clean_screen(self):
    os.system("cls")
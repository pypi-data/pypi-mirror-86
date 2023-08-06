from .Const import *
import os.path
import json

# This class is in charge of managing the scores file.
class Score():
  def __init__(self):
      self.score_file_name = SCORES_FILE_NAME

  def read_score(self):
      if os.path.isfile(self.score_file_name):
        try:
          score_file = open(self.score_file_name)
          dictionary = json.load(score_file)
          score_value = dictionary.get(SCORES_LABEL, 0)
          score_file.close()
          return score_value
        except:
          return BAD_RETURN_CODE
      else:
        return 0

  def add_score(self, difficulty):
      current_score = self.read_score() # score from the file
      if current_score >= 0: # in case of good reading from the file
        new_score = current_score + self.calc_new_score(difficulty)
      else: # in case of bad reading from the file or no file
        new_score = self.calc_new_score(difficulty)

      # Save score in dict to the file
      dictionary = {SCORES_LABEL: new_score} # score value
      try: # file handle
          score_file = open(self.score_file_name, 'wt')
          json.dump(dictionary, score_file)  # save as JSON
          score_file.close()
          return GOOD_RETURN_CODE
      except:
          return BAD_RETURN_CODE

  def calc_new_score(self, difficulty):
      return (difficulty * 3) + 5


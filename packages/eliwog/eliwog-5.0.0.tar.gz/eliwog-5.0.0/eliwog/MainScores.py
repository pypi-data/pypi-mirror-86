from flask import Flask, render_template
from Score import Score

game_score = Score()

app = Flask(__name__)

@app.route('/')


def homepage():
    current_score = game_score.read_score()
    if current_score == -1:
      return render_template('error.html', ERROR=current_score)
    else:
      return render_template('index.html', SCORE=current_score)

if __name__ == '__main__':
    app.run()
else:
    print('Please run this file as main, not as module.')

import os
import sys
import json

# import requests
from flask import Flask, request, jsonify

from play_new_game import play_game
from models_service import get_levels, update_levels
from user_level_model import user_level
import random

app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
  # when the endpoint is registered as a webhook, it must echo back
  # the 'hub.challenge' value it receives in the query arguments

  # if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
  #   if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
  #     return "Verification token mismatch", 403
  #   return request.args["hub.challenge"], 200

  return "Hello world", 200


@app.route('/golfgame-api/getlevels', methods=['GET'])
def webhook1():
  params = request.json
  print(params)
  if 'username' in params:
    user_name = params['username']
    if user_name != "All":
      return get_levels(user_name), 200
    else:
      return "No username", 200
  else:
    return "No params", 200

@app.route('/golfgame-api/updatelevels', methods=['POST'])
def webhook2():
  params = request.json
  print(params)
  if 'username' in params:
    user_name = params['username']
    if user_name != "All":
      random_levels = [random.randint(1,10) for r in range(10)]
      user = user_level(user_name, random_levels)
      update_levels(user)
      return jsonify({"username": user_name, "levels": random_levels}), 200
    else:
      return "No username", 200
  
  return "No params", 200

@app.route('/golfgame-api/playgame', methods=['POST'])
def webhook():
  params = request.json
  hole = params['hole']
  user_name = params['username']

  game = play_game(hole, user_name)
  game_data = game.start_game()
  if game_data:
    return json.dumps(game_data), 200 
  else:
    return "No game data", 200

  return "OK", 200


def log(message):  # simple wrapper for logging to stdout on heroku
  print(message)
  sys.stdout.flush()


if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0')
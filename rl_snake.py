import typing
from stable_baselines import PPO2
import gym_battlesnake
import rl_utils

model = PPO2.load("models/ppo2_trainedmodel_2")

def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "group6",
        "color": "#4806ba",
        "head": "caffeine",
        "tail": "do-sammy",
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")
    print("MODEL LOADED")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:
    moves = ["up", "down", "left", "right"]
    global model
    
    obs = rl_utils.create_observation(game_state)
    action, _ = model.predict(obs)
    print(f"action: {action}")
    
    return {"move": moves[action[0]]}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})


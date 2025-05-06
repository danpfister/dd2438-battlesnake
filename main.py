# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing
import utils
import food
import floodfill

FOOD_WEIGHT = 0.9

# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "danpfister",
        "color": "#4806ba",
        "head": "caffeine",
        "tail": "do-sammy",
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:
    moves = {"up": (0, 1), "down": (0, -1), "left": (-1, 0), "right": (1, 0)}

    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    
    free_fields = utils.get_free_fields(game_state)

    # choose food with lowest food distance
    # next_move = min(safe_moves, key=safe_moves.get)

    # choose position with highest flood fill distance
    safe_moves = []
    floodfill_distances = {}
    food_distances = {}
    for move in moves.keys():
        next_head_pos = (
            my_head["x"] + moves[move][0],
            my_head["y"] + moves[move][1]
        )
        if next_head_pos in free_fields:
            safe_moves.append(move)
            floodfill_distances[move] = floodfill.flood_fill_max_area(game_state, next_head_pos, move)
            food_distances[move] = food.get_food_distance(game_state, next_head_pos)
            #print(f"Flood fill distance for {move}: {floodfill_distances[move]}")
    
    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    scores = {}
    for move in safe_moves:
        if game_state["you"]["health"] < 25:
            scores[move] = max(0, 20 - food_distances[move])
        else:
            scores[move] = FOOD_WEIGHT * max(0, 50 - food_distances[move]) + (1 - FOOD_WEIGHT) * floodfill_distances[move]
        
    next_move = max(scores, key=scores.get)
    #print(f"max_distance: {floodfill_distances[next_move]}")

    print(f"ff distances: {floodfill_distances}")
    print(f"food distances: {food_distances}")
    print(f"scores: {scores}")
    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})

import typing

FOOD_WEIGHT = 0.6

def get_free_fields(game_state: dict):
    fields = set(
        (i, j)
        for i in range(game_state["board"]["width"])
        for j in range(game_state["board"]["height"])
    )
    moves = {"up": (0, 1), "down": (0, -1), "left": (-1, 0), "right": (1, 0)}
    my_length = game_state["you"]["length"]
    
    for b in game_state["you"]["body"]:
        fields.discard((b["x"], b["y"]))
        
    for snake in game_state["board"]["snakes"]:
        if snake["id"] == game_state["you"]["id"]: continue
        head = snake["body"][0]
        
        if snake["length"] >= my_length: # for longer snakes discard cells where enemy head can move
            for move in moves.values():
                fields.discard((head["x"] + move[0], head["y"] + move[1]))
                
        for b in snake["body"]:
            fields.discard((b["x"], b["y"]))
            
    return fields

def get_scores(game_state: dict, food_distances: dict, floodfill_distances: dict):
    # scale values to [0-1]
    max_food_distance = max(max(food_distances.values()), 1)
    food_distances = {k: max(0, 10 - v) / max_food_distance for k, v in food_distances.items()}
    
    max_floodfill_distance = max(max(floodfill_distances.values()), 1)
    floodfill_distances = {k: (v - 5) / max_floodfill_distance for k, v in floodfill_distances.items()}
    
    # TODO add fixed rules or something
    scores = {}
    for move in food_distances.keys():
        scores[move] = FOOD_WEIGHT * food_distances[move] + (1 - FOOD_WEIGHT) * floodfill_distances[move]
    
    return scores
import typing

def get_free_fields(game_state):
    fields = set((i, j) for i in range(11) for j in range(11))
    moves = {"up": (0, 1), "down": (0, -1), "left": (-1, 0), "right": (1, 0)}
    
    for b in game_state["you"]["body"]:
        fields.discard((b["x"], b["y"]))
        
    for snake in game_state["board"]["snakes"]:
        if snake["id"] == game_state["you"]["id"]: continue
        head = snake["body"][0]
        for move in moves.values(): # ignore cells where enemy head can move
            fields.discard((head["x"] + move[0], head["y"] + move[1]))
        for b in snake["body"]:
            fields.discard((b["x"], b["y"]))
            
    return fields
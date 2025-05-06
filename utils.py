import typing

def get_free_fields(game_state):
    fields = set((i, j) for i in range(11) for j in range(11))
    
    for b in game_state["you"]["body"]:
        fields.discard((b["x"], b["y"]))
        
    for snake in game_state["board"]["snakes"]:
        for b in snake["body"]:
            fields.discard((b["x"], b["y"]))
            
    return fields
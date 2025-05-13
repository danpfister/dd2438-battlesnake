import numpy as np

def create_observation(game_state: dict):
    HEIGHT = game_state["board"]["height"]
    WIDTH = game_state["board"]["width"]
    obs =  np.zeros((HEIGHT, WIDTH, 6), dtype=np.uint8)
    
    # layer0: snake health on heads {0,...,100}
    # layer1: snake bodies {0,1}
    # layer2: segment numbers {0,...,255}
    # layer3: snake length >= player {0,1}
    # layer4: food {0,1}
    # layer5: gameboard {0,1}
    
    # layer 0
    my_health = game_state["you"]["health"]
    my_head = game_state["you"]["head"]
    obs[my_head["x"], my_head["y"], 0] = my_health
    
    for snake in game_state["board"]["snakes"]:
        for i, b in enumerate(snake["body"]):
            obs[b["x"], b["y"], 1] = 1 # layer 1
            obs[b["x"], b["y"], 2] = i # layer 2
        
        if snake["health"] > my_health:
            head = snake["head"]
            obs[head["x"], head["y"], 3] = 1 # layer 3
    
    for food in game_state["board"]["food"]:
        obs[food["x"], food["y"], 4] = 1 # layer 4
    
    obs[:, :, 5] = 1 # layer 5
    
    return obs.reshape((1, HEIGHT, WIDTH, 6))
# game_state.py
from constants import W, pwidth, H

pspeed = 6
shield = False
lives  = 3

def reset(pspeed_val=6):
    global lives, shield
    lives  = 3
    shield = False
    return {
        "px":                  W // 2 - pwidth // 2,
        "py":                  H - 80,
        "bullets":             [],
        "enemies":             [],
        "score":               0,
        "powerup_timer":       0,
        "powerup_spawn_timer": 0,
        "powerup_next":        300,
        "timer":               0,
        "combo":               0,
        "lives":               3,
        "powerups":            [],
        "new_record":          False,
        "laser_powerup":       False,
        "pspeed":              pspeed_val,
    }

# constants.py — All constants and configuration

# SCREEN
W, H = 800, 600

# COLORS
BLACK  = (0,   0,   0  )
WHITE  = (255, 255, 255)
RED    = (255, 50,  50 )
GREEN  = (50,  255, 50 )
BLUE   = (50,  150, 255)
YELLOW = (255, 215, 0  )

# CLOCK
FPS = 60

# PLAYER
pwidth, pheight = 60, 20
MIN_SPEED, MAX_SPEED = 2, 12

# BULLET
bullet_speed = 8
fire_gap     = 10

# ENEMY
enemy_size = 65

# DIFFICULTY
diff_data = {
    "Easy":    {"speed": 2, "spawn": 60, "mult": 1},
    "Medium":  {"speed": 3, "spawn": 40, "mult": 1},
    "Hard":    {"speed": 4, "spawn": 30, "mult": 2},
    "Extreme": {"speed": 6, "spawn": 20, "mult": 3},
}

# SCORES FILE
score_file = "scores.txt"

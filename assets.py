# assets.py — Load all images, sounds, fonts, music

import pygame
import os
from constants import enemy_size, pwidth, pheight

# ── IMAGE BASE PATH (relative to main.py) ──────────────────────────────────
BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
IMG_PATH     = os.path.join(BASE_DIR, "img png")
POWERUP_PATH = os.path.join(BASE_DIR, "powerup")

def load_images():
    """Load and scale all game images. Returns a dict."""
    player_img = pygame.image.load(os.path.join(IMG_PATH, "player.png")).convert_alpha()
    player_img = pygame.transform.scale(player_img, (pwidth, pheight))

    raw_enemies = [
        pygame.image.load(os.path.join(IMG_PATH, "enemy1.png")).convert_alpha(),
        pygame.image.load(os.path.join(IMG_PATH, "enemy2.png")).convert_alpha(),
        pygame.image.load(os.path.join(IMG_PATH, "enemy3.png")).convert_alpha(),
    ]
    enemy_images = [pygame.transform.scale(img, (enemy_size, enemy_size)) for img in raw_enemies]

    boss_img = pygame.image.load(os.path.join(IMG_PATH, "boss.png")).convert_alpha()
    boss_img = pygame.transform.scale(boss_img, (enemy_size * 2, enemy_size * 2))

    shield_img = pygame.image.load(os.path.join(POWERUP_PATH, "shield.png")).convert_alpha()
    shield_img = pygame.transform.scale(shield_img, (35, 35))

    laser_img = pygame.image.load(os.path.join(POWERUP_PATH, "laser.png")).convert_alpha()
    laser_img = pygame.transform.scale(laser_img, (35, 35))

    speed_img = pygame.image.load(os.path.join(POWERUP_PATH, "speed.png")).convert_alpha()
    speed_img = pygame.transform.scale(speed_img, (35, 35))

    return {
        "player":       player_img,
        "enemy_images": enemy_images,
        "boss":         boss_img,
        "shield":       shield_img,
        "laser":        laser_img,
        "speed":        speed_img,
    }


def load_sounds():
    """Load all sound effects. Returns a dict."""
    base = BASE_DIR
    return {
        "shoot":    pygame.mixer.Sound(os.path.join(base, "shoot.wav")),
        "hit":      pygame.mixer.Sound(os.path.join(base, "hit.wav")),
        "over":     pygame.mixer.Sound(os.path.join(base, "gameover.wav")),
        "powerup":  pygame.mixer.Sound(os.path.join(base, "powerup.wav")),
    }


def load_music():
    """Load and start looping background music."""
    pygame.mixer.music.load(os.path.join(BASE_DIR, "bg.mp3"))
    pygame.mixer.music.play(-1)


def load_fonts():
    """Return a dict of fonts."""
    return {
        "font":  pygame.font.SysFont("arial", 26),
        "big":   pygame.font.SysFont("arial", 48),
        "small": pygame.font.SysFont("arial", 20),
    }

# gameplay.py

import pygame
import random
from constants import W, H, WHITE, RED, GREEN, YELLOW, BLUE, bullet_speed, fire_gap, diff_data
from draw_utils import draw_player
from scores import save_scores

POWERUP_MIN_INTERVAL = 300   # 5s
POWERUP_MAX_INTERVAL = 600   # 10s

# Laser beam state — each beam: {cx, cy_start, timer, max_timer}
_laser_beams = []


def build_enemy_types(enemy_images):
    return [
        {"img": enemy_images[0], "size": 60, "speed": 3, "points": 1},
        {"img": enemy_images[1], "size": 50, "speed": 5, "points": 2},
        {"img": enemy_images[2], "size": 80, "speed": 2, "points": 3},
    ]


def _draw_powerup_icon(screen, pu):
    t     = pygame.time.get_ticks()
    pulse = abs((t % 800) - 400) / 400
    alpha = int(80 + 175 * pulse)
    col   = {"shield": (50, 255, 50), "laser": (255, 215, 0), "speed": (50, 150, 255)}[pu["type"]]
    glow  = pygame.Surface((45, 45), pygame.SRCALPHA)
    pygame.draw.rect(glow, (*col, alpha), (0, 0, 45, 45), border_radius=8)
    screen.blit(glow, (pu["rect"].x - 5, pu["rect"].y - 5))
    screen.blit(pu["img"], (pu["rect"].x, pu["rect"].y))


def _draw_heart(screen, cx, cy, size, color):
    """Draw a proper heart shape using circles + triangle."""
    r = size // 2
    # Two circles for top bumps
    pygame.draw.circle(screen, color, (cx - r//2, cy - r//4), r//2)
    pygame.draw.circle(screen, color, (cx + r//2, cy - r//4), r//2)
    # Triangle for bottom point
    pygame.draw.polygon(screen, color, [
        (cx - r, cy - r//4),
        (cx + r, cy - r//4),
        (cx,     cy + r),
    ])


def _fire_laser(game, float_texts):
    """Fire a laser beam from player center upward."""
    cx       = game["px"] + 30          # horizontal center of player
    cy_start = game["py"]               # top of player — beam starts here
    MAX_T    = 25   # ~0.4s visible at 60fps
    _laser_beams.append({"cx": cx, "cy_start": cy_start,
                          "timer": MAX_T, "max_timer": MAX_T})


def _update_laser_beams(screen, game, enemies, float_texts, settings, snd):
    """Draw beams rising from player top and kill enemies hit."""
    for beam in _laser_beams[:]:
        beam["timer"] -= 1
        frac  = beam["timer"] / beam["max_timer"]   # 1→0 as beam fades
        alpha = int(255 * frac)

        cx       = beam["cx"]
        cy_start = beam["cy_start"]      # beam bottom (player top)
        cy_end   = 0                     # beam goes to screen top

        beam_h = cy_start - cy_end       # height of beam strip

        # Outer glow (wide, semi-transparent)
        glow = pygame.Surface((16, beam_h), pygame.SRCALPHA)
        glow.fill((255, 200, 0, int(60 * frac)))
        screen.blit(glow, (cx - 8, cy_end))

        # Main beam body
        body = pygame.Surface((8, beam_h), pygame.SRCALPHA)
        body.fill((255, 220, 50, alpha))
        screen.blit(body, (cx - 4, cy_end))

        # Bright white core
        core = pygame.Surface((3, beam_h), pygame.SRCALPHA)
        core.fill((255, 255, 255, alpha))
        screen.blit(core, (cx - 1, cy_end))

        # Muzzle flash at player top
        mf_r = int(10 * frac) + 4
        mf_s = pygame.Surface((mf_r*2, mf_r*2), pygame.SRCALPHA)
        pygame.draw.circle(mf_s, (255, 255, 100, alpha), (mf_r, mf_r), mf_r)
        screen.blit(mf_s, (cx - mf_r, cy_start - mf_r))

        # Kill enemies in beam path
        beam_rect = pygame.Rect(cx - 4, cy_end, 8, beam_h)
        for en in enemies[:]:
            if beam_rect.colliderect(en["rect"]):
                if settings.get("sound", True): snd["hit"].play()
                enemies.remove(en)
                pts = en["points"]
                game["score"] += pts
                game["combo"]  = game.get("combo", 0) + 1
                float_texts.append({"text": f"+{pts}", "x": en["rect"].x,
                                    "y": en["rect"].y, "t": 35})

        if beam["timer"] <= 0:
            _laser_beams.remove(beam)


def update_game(screen, game, state, difficulty, scores,
                snd, fonts, float_texts, shield_ref,
                imgs, enemy_types, fire_time_ref, settings):

    shield    = shield_ref
    fire_time = fire_time_ref
    font      = fonts["font"]
    small     = fonts["small"]
    keys      = pygame.key.get_pressed()
    pspeed    = game.get("pspeed", 6)

    # ── MOVEMENT ──────────────────────────────────────────────────────────────
    if keys[pygame.K_a] and game["px"] > 0:       game["px"] -= pspeed
    if keys[pygame.K_d] and game["px"] < W - 60:  game["px"] += pspeed

    # ── SHOOTING — laser mode fires a beam, normal mode fires bullets ─────────
    fire_time += 1
    laser_mode = game.get("laser_powerup", False)

    if fire_time >= fire_gap and (keys[pygame.K_SPACE] or keys[pygame.K_w]):
        if laser_mode:
            _fire_laser(game, float_texts)
            if settings.get("sound", True): snd["shoot"].play()
        else:
            game["bullets"].append(pygame.Rect(game["px"] + 30, game["py"], 6, 15))
            if settings.get("sound", True): snd["shoot"].play()
        fire_time = 0

    # ── DRAW PLAYER ───────────────────────────────────────────────────────────
    p = draw_player(screen, imgs["player"], game["px"], game["py"])

    # Shield glow around player
    if shield:
        t  = pygame.time.get_ticks()
        r  = int(38 + 6 * abs((t % 800) - 400) / 400)
        cx = game["px"] + 30
        cy = game["py"] + 10
        gs = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
        pygame.draw.circle(gs, (50, 255, 50, 55), (r, r), r)
        pygame.draw.circle(gs, (50, 255, 50, 180), (r, r), r, 2)
        screen.blit(gs, (cx - r, cy - r))

    # ── LASER BEAMS — drawn after player so beam starts at player top ────────
    if laser_mode:
        _update_laser_beams(screen, game, game["enemies"], float_texts,
                            settings, snd)

    # ── BULLETS ───────────────────────────────────────────────────────────────
    for b in game["bullets"][:]:
        b.y -= bullet_speed
        pygame.draw.rect(screen, WHITE, b)
        if b.y < 0: game["bullets"].remove(b)

    # ── SPAWN ENEMIES ─────────────────────────────────────────────────────────
    game["timer"] += 1
    if game["timer"] > diff_data[difficulty]["spawn"]:
        etype = random.choice(enemy_types)
        game["enemies"].append({
            "rect":   pygame.Rect(random.randint(0, W - etype["size"]),
                                  -etype["size"], etype["size"], etype["size"]),
            "img":    etype["img"],
            "speed":  etype["speed"],
            "points": etype["points"],
        })
        game["timer"] = 0

    # ── GUARANTEED POWERUP SPAWN ──────────────────────────────────────────────
    game["powerup_spawn_timer"] = game.get("powerup_spawn_timer", 0) + 1
    if game["powerup_spawn_timer"] >= game.get("powerup_next", POWERUP_MIN_INTERVAL):
        ptype = random.choice(["shield", "speed", "laser"])
        game["powerups"].append({
            "type": ptype, "img": imgs[ptype],
            "rect": pygame.Rect(random.randint(40, W - 70), -35, 35, 35),
        })
        game["powerup_spawn_timer"] = 0
        game["powerup_next"] = random.randint(POWERUP_MIN_INTERVAL, POWERUP_MAX_INTERVAL)

    # ── SHIELD — protects entire bottom edge ──────────────────────────────────
    shield_bar = pygame.Rect(0, H - 4, W, 4)   # full-width base bar
    if shield:
        t     = pygame.time.get_ticks()
        pulse = int(100 + 100 * abs((t % 600) - 300) / 300)
        pygame.draw.rect(screen, (0, pulse, 0), shield_bar)

    # ── ENEMIES ───────────────────────────────────────────────────────────────
    for en in game["enemies"][:]:
        en["rect"].y += en["speed"]
        screen.blit(en["img"], (en["rect"].x, en["rect"].y))

        # Reached bottom
        if en["rect"].y >= H - 4:
            game["enemies"].remove(en)
            game["combo"] = 0
            if shield:
                # Shield absorbs ONE bottom hit, then breaks
                shield = False
                float_texts.append({"text": "BASE PROTECTED!", "x": W//2 - 70,
                                    "y": H - 60, "t": 80, "color": GREEN})
            else:
                game["lives"] -= 1
                if game["lives"] <= 0:
                    if settings.get("sound", True): snd["over"].play()
                    if game["score"] > scores[difficulty]:
                        game["new_record"] = True
                        scores[difficulty] = game["score"]
                        save_scores(scores)
                    state = "OVER"
            continue

        # Bullet hit
        for b in game["bullets"][:]:
            if en["rect"].colliderect(b):
                if settings.get("sound", True): snd["hit"].play()
                game["enemies"].remove(en)
                game["bullets"].remove(b)
                pts = en["points"]
                game["score"] += pts
                game["combo"]  = game.get("combo", 0) + 1
                float_texts.append({"text": f"+{pts}", "x": en["rect"].x,
                                    "y": en["rect"].y, "t": 40})
                break

        # Player collision
        if en in game["enemies"] and en["rect"].colliderect(p):
            game["enemies"].remove(en)
            if shield:
                shield = False
                float_texts.append({"text": "SHIELD BREAK!", "x": game["px"],
                                    "y": game["py"] - 30, "t": 60, "color": GREEN})
            else:
                game["lives"] -= 1
                if game["lives"] <= 0:
                    if settings.get("sound", True): snd["over"].play()
                    if game["score"] > scores[difficulty]:
                        game["new_record"] = True
                        scores[difficulty] = game["score"]
                        save_scores(scores)
                    state = "OVER"

    # ── FLOAT TEXTS ───────────────────────────────────────────────────────────
    for ft in float_texts[:]:
        screen.blit(small.render(ft["text"], True, ft.get("color", YELLOW)),
                    (ft["x"], ft["y"]))
        ft["y"] -= 1; ft["t"] -= 1
        if ft["t"] <= 0: float_texts.remove(ft)

    # ── POWERUPS ──────────────────────────────────────────────────────────────
    for pu in game["powerups"][:]:
        _draw_powerup_icon(screen, pu)
        pu["rect"].y += 2

        if pu["rect"].colliderect(p):
            if settings.get("sound", True): snd["powerup"].play()
            if pu["type"] == "shield":
                shield = True
                game["powerup_timer"] = 600          # 10s
                float_texts.append({"text": "SHIELD ON! Base Protected!",
                                    "x": W//2 - 120, "y": H//2, "t": 100, "color": GREEN})
            elif pu["type"] == "laser":
                game["laser_powerup"]  = True
                game["powerup_timer"]  = 360         # 6s
                _laser_beams.clear()
                float_texts.append({"text": "LASER MODE!", "x": W//2 - 60,
                                    "y": H//2, "t": 90, "color": YELLOW})
            elif pu["type"] == "speed":
                game["pspeed"] = min(12, game.get("pspeed", 6) + 2)
                float_texts.append({"text": "SPEED UP!", "x": W//2 - 50,
                                    "y": H//2, "t": 80, "color": (50, 150, 255)})
            game["powerups"].remove(pu)
        elif pu["rect"].y > H:
            game["powerups"].remove(pu)

    # ── POWERUP TIMER ─────────────────────────────────────────────────────────
    if game["powerup_timer"] > 0:
        game["powerup_timer"] -= 1
        if game["powerup_timer"] == 0:
            if shield:
                shield = False
                float_texts.append({"text": "SHIELD EXPIRED", "x": W//2 - 70,
                                    "y": H//2, "t": 60, "color": RED})
            if game.get("laser_powerup"):
                game["laser_powerup"] = False
                _laser_beams.clear()

    # ── HUD ───────────────────────────────────────────────────────────────────
    from draw_utils import text as dt
    dt(screen, f"Score : {game['score']}", 10, 10, f=font)
    dt(screen, f"Level : {difficulty}",    10, 40, f=font)

    # Lives as heart icons
    for i in range(game["lives"]):
        _draw_heart(screen, 665 + i * 32, 20, 20, RED)

    if game.get("combo", 0) >= 3:
        dt(screen, f"COMBO x{game['combo']}", 10, 70, YELLOW, font)

    if game["powerup_timer"] > 0:
        secs = game["powerup_timer"] // 60
        if shield:
            dt(screen, f"SHIELD : {secs}s", 10, 100, GREEN, font)
        elif game.get("laser_powerup"):
            dt(screen, f"LASER  : {secs}s", 10, 100, YELLOW, font)

    # Next powerup countdown
    fl = max(0, game.get("powerup_next", POWERUP_MIN_INTERVAL) - game.get("powerup_spawn_timer", 0))
    dt(screen, f"Powerup in: {fl//60}s", W - 190, 10, (140, 140, 220), font)

    return state, fire_time, shield, float_texts, scores

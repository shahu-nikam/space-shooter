# scores.py — High-score load / save

import os

# On Android, we must write to a writable location
try:
    from android.storage import app_storage_path  # type: ignore
    _SCORE_DIR = app_storage_path()
except ImportError:
    _SCORE_DIR = os.path.dirname(os.path.abspath(__file__))

score_file = os.path.join(_SCORE_DIR, "scores.txt")


def load_scores():
    """Read scores from file. Returns dict with default 0 for each difficulty."""
    scores = {"Easy": 0, "Medium": 0, "Hard": 0, "Extreme": 0}
    if os.path.exists(score_file):
        for line in open(score_file):
            line = line.strip()
            if ":" in line:
                k, v = line.split(":", 1)
                scores[k] = int(v)
    return scores


def save_scores(scores):
    """Write scores dict back to file."""
    with open(score_file, "w") as f:
        for k in scores:
            f.write(f"{k}:{scores[k]}\n")

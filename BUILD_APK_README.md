# 📱 Space Shooter — APK Build Guide

## What was changed (game code untouched)
| File | Change |
|------|--------|
| `assets.py` | Replaced hardcoded `E:\games\...` Windows paths with `os.path` relative paths |
| `scores.py` | Score file now saves to a writable directory on Android |
| `buildozer.spec` | **New file** — tells Buildozer how to build your APK |
| `BUILD_APK_README.md` | **New file** — this guide |

All gameplay, graphics, sounds, logic = 100% unchanged.

---

## 🛠️ How to Build the APK

Buildozer only runs on **Linux** (Ubuntu/Debian recommended).  
Use **WSL2** on Windows, or a Linux VM, or a cloud machine.

### Step 1 — Install dependencies

```bash
sudo apt update && sudo apt install -y \
    python3-pip python3-venv git zip unzip \
    openjdk-17-jdk autoconf libtool pkg-config \
    zlib1g-dev libncurses5-dev libncursesw5-dev \
    libtinfo5 cmake libffi-dev libssl-dev
```

### Step 2 — Install Buildozer

```bash
pip3 install --user buildozer cython
```

### Step 3 — Copy your project to Linux

Copy the entire `SPACE_SHOOTER_APK` folder to your Linux machine.

### Step 4 — Build the APK

```bash
cd SPACE_SHOOTER_APK
buildozer android debug
```

First build downloads Android SDK/NDK (~2 GB) and takes **20–40 minutes**.  
After that, rebuilds are much faster.

### Step 5 — Install on your phone

```bash
# With USB debugging ON and phone connected:
buildozer android deploy run

# OR find the APK at:
# bin/spaceshooter-1.0-debug.apk
# and transfer it to your phone manually.
```

---

## ☁️ Build Online (No Linux Needed)

Use **Google Colab** (free):

1. Open https://colab.research.google.com
2. Create a new notebook and run:

```python
# Install buildozer
!pip install buildozer cython

# Install system deps
!apt-get install -y \
    openjdk-17-jdk autoconf libtool pkg-config \
    zlib1g-dev libncurses5-dev cmake libffi-dev libssl-dev

# Upload your zip, then:
import zipfile
zipfile.ZipFile('SPACE_SHOOTER_APK.zip').extractall('game')
%cd game

# Build!
!buildozer android debug
```

3. Download the `.apk` from the `bin/` folder.

---

## 📲 Install the APK on Android

1. Transfer the `.apk` file to your phone
2. Go to **Settings → Security → Install Unknown Apps** and allow your file manager
3. Tap the `.apk` file to install
4. Launch **Space Shooter** 🚀

---

## ⚙️ Customizing `buildozer.spec`

| Setting | What it does |
|---------|-------------|
| `title` | App name shown on phone |
| `version` | App version number |
| `android.api = 33` | Target Android API level |
| `android.minapi = 21` | Minimum Android 5.0+ |
| `android.archs` | CPU architectures (arm64 + arm covers 99% of phones) |
| `fullscreen = 1` | Game runs fullscreen |

---

## ❓ Troubleshooting

**"SDL_Init failed"** — Make sure `pygame_ce` is in requirements (not plain `pygame`)  
**Sound doesn't work** — Some Android versions need `AUDIO` permission; add to `android.permissions`  
**Black screen** — Check that all asset paths load correctly; test on desktop first with `python main.py`

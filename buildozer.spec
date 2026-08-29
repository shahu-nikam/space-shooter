[app]
# App name and package
title = Space Shooter
package.name = spaceshooter
package.domain = org.game

# Source
source.dir = .
source.include_exts = py,png,jpg,wav,mp3,txt

# Version
version = 1.0

# Entry point
entrypoint = main.py

# Requirements — pygame-ce is the maintained fork that works best on Android
requirements = python3,pygame_ce

# Orientation
orientation = landscape

# Android specific
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

# Fullscreen
fullscreen = 1

# Icon (uses player.png as placeholder — replace with a 512x512 icon for Play Store)
# icon.filename = %(source.dir)s/img png/player.png

[buildozer]
log_level = 2
warn_on_root = 1

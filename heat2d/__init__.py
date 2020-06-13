"""
      HEAT2D Game Engine
     GPL 3.0 © Kadir Aksoy
https://github.com/kadir014/heat2d

"""

VERSION =       "0.0.2"
VERSION_TUPLE = (0, 0, 1)
VERSION_STATE = "alpha"
LICENSE =       "GNU General Public License v3.0"

import sys
PLATFORM = None
if   sys.platform == "win32": PLATFORM = "Windows"
elif sys.platform == "darwin":  PLATFORM = "MacOS"
elif sys.platform.startswith("linux"): PLATFORM = "Linux"
elif sys.platform.startswith("freebsd"): PLATFORM = "FreeBSD"

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
import pygame

DISPATCHER = dict()
THREADS = list()
TOTAL_THREADS = 0

if "HEAT2D_DISABLE_ANSI_COLORS" in os.environ: __USE_ANSI_COLORS = False
else: __USE_ANSI_COLORS = True

from heat2d.libs.terminal import REVERSE, RESET, FG
if "HEAT2D_HIDE_WELCOME_MESSAGE" not in os.environ:
    if __USE_ANSI_COLORS:
        print(f"\u2588{REVERSE}" + "\u2584"*20 + f"{RESET}\u2588")
        print(f"\u2588{FG.lightred}       HEAT2D       {RESET}\u2588 Heat2D Version: 0.0.0")
        print(f"\u2588{FG.orange}    GAME ENGINE     {RESET}\u2588 Pygame Version: {pygame.version.ver}")
        print("\u2588" + "\u2584"*20 + "\u2588\n")
    else:
        print(f"\u2588{REVERSE}" + "\u2584"*20 + f"{RESET}\u2588")
        print(f"\u2588       HEAT2D       \u2588 Heat2D Version: 0.0.0")
        print(f"\u2588    GAME ENGINE     \u2588 Pygame Version: {pygame.version.ver}")
        print("\u2588" + "\u2584"*20 + "\u2588\n")

from heat2d.engine import Engine
from heat2d.stage import Stage
from heat2d.gameobject import GameObject
from heat2d.sprite import Sprite
from heat2d import visuals
from heat2d.timer import Timer, TickTimer
from heat2d import ui
from heat2d import postprocess
from heat2d import networking

del sys, os, pygame, libs, engine, errors, window, gameobject, renderer, sprite, stage, timer, REVERSE, RESET, FG

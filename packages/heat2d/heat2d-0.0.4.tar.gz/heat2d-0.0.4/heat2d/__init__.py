#       HEAT2D Game Engine
#      GPL 3.0 © Kadir Aksoy
#https://github.com/kadir014/heat2d

import os

from heat2d.libs import utils

from heat2d.libs import specs
specs.OS.update_info()
if "HEAT2D_UPDATE_SPECS_INFO" not in os.environ: os.environ["HEAT2D_UPDATE_SPECS_INFO"] = "1"
if os.environ["HEAT2D_UPDATE_SPECS_INFO"] == "1":
    print("You can see all by using 'heat2d.specs.print_specs()'\n")
    print("Gathering RAM information...")
    specs.RAM.update_info()
    print("Gathering CPU information...")
    specs.CPU.update_info()
    print("Gathering disk information...")
    specs.Disk.update_info()

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
import pygame

class DISPATCHER: pass

if "HEAT2D_DISABLE_ANSI_COLORS" in os.environ: __USE_ANSI_COLORS = False
else: __USE_ANSI_COLORS = True

from heat2d.libs.terminal import REVERSE, RESET, FG, clear

clear()

from heat2d.version import *

from heat2d.libs.color import Color, Palette
from heat2d.engine import     Engine
from heat2d.stage import      Stage
from heat2d.gameobject import GameObject
from heat2d.sprite import     Sprite
from heat2d.timer import      Timer
from heat2d import            audio
from heat2d import            ui
from heat2d import            gl
from heat2d import            networking
from heat2d.math import       Vector2

if "HEAT2D_HIDE_WELCOME_MESSAGE" not in os.environ:
    if __USE_ANSI_COLORS:
        print(f"\u2588" + "\u2580"*20 + f"\u2588")
        print(f"\u2588{FG.lightred}       HEAT2D       {RESET}\u2588 Version : {HEAT2D_VERSION}")
        print(f"\u2588{FG.orange}    GAME ENGINE     {RESET}\u2588 State   : {HEAT2D_VERSION_STATE.capitalize()}")
        print("\u2588" + "\u2584"*20 + "\u2588\n")
    else:
        print(f"\u2588" + "\u2580"*20 + f"\u2588")
        print(f"\u2588       HEAT2D       \u2588 Version : {HEAT2D_VERSION}")
        print(f"\u2588    GAME ENGINE     \u2588 State   : {HEAT2D_VERSION_STATE.capitalize()}")
        print("\u2588" + "\u2584"*20 + "\u2588\n")

del os, pygame, libs, engine, errors, window, gameobject, renderer, sprite, stage, timer, math, REVERSE, RESET, FG

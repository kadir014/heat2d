from heat2d import __USE_ANSI_COLORS
from heat2d.libs.terminal import RESET, FG


def warn(message):
    if __USE_ANSI_COLORS: print(f"{FG.orange}WARNING:{RESET} {message}")
    else: print(f"WARNING: {message}")

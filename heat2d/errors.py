#  This file is a part of the Heat2D Project and  #
#  distributed under the LGPL 3 license           #
#                                                 #
#           HEAT2D Game Engine Project            #
#            Copyright © Kadir Aksoy              #
#       https://github.com/kadir014/heat2d        #


from heat2d import __USE_ANSI_COLORS
from heat2d.libs.terminal import RESET, FG


def warn(message):
    if __USE_ANSI_COLORS: print(f"{FG.orange}WARNING:{RESET} {message}")
    else: print(f"WARNING: {message}")



class NoStageDeclared(Exception): pass
class UnknownKey(Exception): pass
class UnknownMouseButton(Exception): pass
class UnknownControllerButton(Exception): pass
class DeviceNotFound(Exception): pass
class NetworkingError(Exception): pass
class AnimationNotMatched(Exception): pass

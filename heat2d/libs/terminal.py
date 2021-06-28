#  This file is a part of the Heat2D Project and  #
#  distributed under the GPL 3 license            #
#                                                 #
#           HEAT2D Game Engine Project            #
#            Copyright © Kadir Aksoy              #
#       https://github.com/kadir014/heat2d        #


from heat2d import specs
import os


def clear():
    if specs.OS.name == "Windows": os.system("cls")
    else: os.system("clear")

#ANSI Escape Graphic Sequences

RESET =     "\033[0m"
BOLD =      "\033[01m"
UNDERLINE = "\033[04m"
REVERSE =   "\033[07m"

def rgb(rgb):
    return f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m"


class FG:
    black =      "\033[30m"
    darkgray =   "\033[90m"
    lightgray =  "\033[37m"
    white =      "\033[97m"
    red =        "\033[31m"
    orange =     "\033[33m"
    yellow =     "\033[93m"
    green =      "\033[32m"
    blue =       "\033[34m"
    cyan =       "\033[36m"
    purple =     "\033[35m"
    magenta =    "\033[95m"
    lightred =   "\033[91m"
    lightgreen = "\033[92m"
    lightblue =  "\033[94m"
    lightcyan =  "\033[96m"


class BG:
    black =      "\033[40m"
    darkgray =   "\033[100m"
    lightgray =  "\033[47m"
    white =      "\033[107m"
    red =        "\033[41m"
    orange =     "\033[43m"
    yellow =     "\033[103m"
    green =      "\033[42m"
    blue =       "\033[44m"
    cyan =       "\033[46m"
    purple =     "\033[45m"
    magenta =    "\033[105m"
    lightred =   "\033[101m"
    lightgreen = "\033[102m"
    lightblue =  "\033[104m"
    lightcyan =  "\033[106m"

#  This file is a part of the Heat2D Project and  #
#  distributed under the GPL 3 license            #
#                                                 #
#           HEAT2D Game Engine Project            #
#            Copyright © Kadir Aksoy              #
#       https://github.com/kadir014/heat2d        #



class Slot:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.empty = True



class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

        self.slots = [[Slot(r, c) for r in range(self.rows)] for c in range(self.cols)]

    def __getitem__(self, pos):
        return self.slots[pos[1]][pos[0]]

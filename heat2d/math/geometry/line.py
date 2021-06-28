#  This file is a part of the Heat2D Project and  #
#  distributed under the LGPL 3 license           #
#                                                 #
#           HEAT2D Game Engine Project            #
#            Copyright © Kadir Aksoy              #
#       https://github.com/kadir014/heat2d        #



class Line:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.normal = (self.end - self.start).perp().normalize()

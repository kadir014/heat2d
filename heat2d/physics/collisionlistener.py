#  This file is a part of the Heat2D Project and  #
#  distributed under the LGPL 3 license           #
#                                                 #
#           HEAT2D Game Engine Project            #
#            Copyright © Kadir Aksoy              #
#       https://github.com/kadir014/heat2d        #



class CollisionListener:
    def __init__(self):
        self.triggers    = False
        self.gameobjects = False
        self.tiles       = False

    def __repr__(self):
        return f"<heat2d.physics.CollisionListener(triggers={self.triggers}, gameobjects={self.gameobjects}, tiles={self.tiles})>"

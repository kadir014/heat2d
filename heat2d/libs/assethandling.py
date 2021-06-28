#  This file is a part of the Heat2D Project and  #
#  distributed under the LGPL 3 license           #
#                                                 #
#           HEAT2D Game Engine Project            #
#            Copyright © Kadir Aksoy              #
#       https://github.com/kadir014/heat2d        #


import threading
import requests



class OnlineAsset(threading.Thread):
    def __init__(self, cache=True):
        super().__init__()

        self.cache = cache



class AssetLoader(threading.Thread):
    def __init__(self, limit=10):
        super().__init__()

        self.limit = limit

        self.tasks = list()

        self.running = False
        self.pause = False

    def __repr__(self):
        return f"<heat2d.AssetLoader({self.name})>"

    def pause(self):
        self.pause = True

    def resume(self):
        self.pause = False

    def toggle_pause(self):
        if self.pause: self.pause = False
        else: self.pause = True

    def run(self):
        while self.running:
            if self.pause: continue

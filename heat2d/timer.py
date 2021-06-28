#  This file is a part of the Heat2D Project and  #
#  distributed under the GPL 3 license            #
#                                                 #
#           HEAT2D Game Engine Project            #
#            Copyright © Kadir Aksoy              #
#       https://github.com/kadir014/heat2d        #


import time

from heat2d import DISPATCHER



class Timer:
    def __init__(self):
        self.funcs = {"every_tick":[], "every_microsec":[], "every_millisec":[],
                      "every_second":[], "every_minute":[], "every_hour":[]}

        DISPATCHER.engine.timers.append(self)

    def __repr__(self):
        return f"<heat2d.Timer()>"

    def every_tick(self, interval, loop=True):
        def inner_decorator(func):
            self.funcs["every_tick"].append({"func":func, "interval":interval, "loop":loop, "done":False, "tick":0})
            return func
        return inner_decorator

    def every_microsec(self, interval, loop=True):
        def inner_decorator(func):
            self.funcs["every_microsec"].append({"func":func, "interval":interval, "loop":loop, "done":False, "last":0, "timef":0})
            return func
        return inner_decorator

    def every_millisec(self, interval, loop=True):
        def inner_decorator(func):
            self.funcs["every_millisec"].append({"func":func, "interval":interval, "loop":loop, "done":False, "last":0, "timef":0})
            return func
        return inner_decorator

    def every_second(self, interval, loop=True):
        def inner_decorator(func):
            self.funcs["every_second"].append({"func":func, "interval":interval, "loop":loop, "done":False, "last":0, "timef":0})
            return func
        return inner_decorator

    def every_minute(self, interval, loop=True):
        def inner_decorator(func):
            self.funcs["every_minute"].append({"func":func, "interval":interval, "loop":loop, "done":False, "last":0, "timef":0})
            return func
        return inner_decorator

    def every_hour(self, interval, loop=True):
        def inner_decorator(func):
            self.funcs["every_hour"].append({"func":func, "interval":interval, "loop":loop, "done":False, "last":0, "timef":0})
            return func
        return inner_decorator

    def update(self):
        for timef in self.funcs["every_tick"]:
            if not timef["done"]:
                timef["tick"] += 1
                if timef["tick"] > timef["interval"]:
                    timef["tick"] = 0
                    timef["func"]()
                    if not timef["loop"]: timef["done"] = True

        for timef in self.funcs["every_microsec"]:
            if not timef["done"]:
                timef["timef"] = (time.time() - timef["last"]) * 1000000
                if timef["timef"] > timef["interval"]:
                    timef["timef"] = 0
                    timef["last"] = time.time()
                    timef["func"]()
                    if not timef["loop"]: timef["done"] = True

        for timef in self.funcs["every_millisec"]:
            if not timef["done"]:
                timef["timef"] = (time.time() - timef["last"]) * 1000
                if timef["timef"] > timef["interval"]:
                    timef["timef"] = 0
                    timef["last"] = time.time()
                    timef["func"]()
                    if not timef["loop"]: timef["done"] = True

        for timef in self.funcs["every_second"]:
            if not timef["done"]:
                timef["timef"] = time.time() - timef["last"]
                if timef["timef"] > timef["interval"]:
                    timef["timef"] = 0
                    timef["last"] = time.time()
                    timef["func"]()
                    if not timef["loop"]: timef["done"] = True

        for timef in self.funcs["every_minute"]:
            if not timef["done"]:
                timef["timef"] = (time.time() - timef["last"]) / 60
                if timef["timef"] > timef["interval"]:
                    timef["timef"] = 0
                    timef["last"] = time.time()
                    timef["func"]()
                    if not timef["loop"]: timef["done"] = True

        for timef in self.funcs["every_hour"]:
            if not timef["done"]:
                timef["timef"] = (time.time() - timef["last"]) / 3600
                if timef["timef"] > timef["interval"]:
                    timef["timef"] = 0
                    timef["last"] = time.time()
                    timef["func"]()
                    if not timef["loop"]: timef["done"] = True

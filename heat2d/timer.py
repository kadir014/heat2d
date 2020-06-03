import time
from heat2d import DISPATCHER


class Timer:

    def __init__(self, interval):
        self.init_time = time.time()
        self.interval = interval
        self.time = 0
        self.func = None

        DISPATCHER["engine"].timers.append(self)

    def __repr__(self):
        return f"heat2d.timer.Timer({self.time} ms)"

    def do(self, func):
        self.func = func

    def update(self):
        self.time = (time.time() - self.init_time) * 1000
        if self.time >= self.interval:
            self.time = 0
            if self.func: self.func()
            self.init_time = time.time()


class TickTimer:

    def __init__(self, interval):
        self.interval = interval
        self.tick = 0
        self.func = None

        DISPATCHER["engine"].timers.append(self)

    def __repr__(self):
        return f"heat2d.timer.TickTimer({self.tick} ticks)"

    def do(self, func):
        self.func = func

    def update(self):
        self.tick += 1
        if self.tick >= self.interval:
            self.tick = 0
            if self.func: self.func()

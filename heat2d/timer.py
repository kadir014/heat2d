import time


class Timer:

    def __init__(self, func, secs):
        self.init_time = time.time()
        self.secs = secs
        self.time = 0
        self.func = func

    def __repr__(self):
        return f"heat2d.timer.Timer({self.time} ms)"

    def update(self):
        self.time = (time.time() - self.init_time) * 1000
        if self.time >= self.secs:
            self.time = 0
            self.func()
            self.init_time = time.time()


class TickTimer:

    def __init__(self, func, ticks):
        self.ticks = ticks
        self.tick = 0
        self.func = func

    def __repr__(self):
        return f"heat2d.timer.TickTimer({self.tick} ticks)"

    def update(self):
        self.tick += 1
        if self.tick >= self.ticks:
            self.tick = 0
            self.func()

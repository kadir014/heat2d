import pygame
from PIL import Image, ImageFilter

#Thanks to St. Paul for the optimization method for blurring

class GaussianBlur:

    def __init__(self, radius=3, resolution=40):
        self.radius = radius
        self.resolution = resolution

    def __repr__(self):
        return f"<heat2d.postprocess.GaussianBlur(radius={self.radius}, resolution={self.resolution})>"

    def process(self, display, size, position):
        surface = pygame.Surface(size)
        surface.blit(display, (0, 0), (position[0], position[1], size[0], size[1]))
        surface = pygame.transform.rotozoom(surface, 0, (self.resolution / 100.0) * 1)
        _size = surface.get_size()
        bytesurf = pygame.image.tostring(surface, "RGBA", False)
        bytesurf = Image.frombytes("RGBA", _size, bytesurf)
        bytesurf = bytesurf.filter(ImageFilter.GaussianBlur(radius=int(self.radius)))
        bytesurf = pygame.image.frombuffer(bytesurf.tobytes(), bytesurf.size, bytesurf.mode).convert()
        bytesurf = pygame.transform.rotozoom(bytesurf, 0, (100.0 / self.resolution) * 1)
        display.blit(bytesurf, position)


class BoxBlur:

    def __init__(self, radius=3, resolution=40):
        self.radius = radius
        self.resolution = resolution

    def __repr__(self):
        return f"<heat2d.postprocess.BoxBlur(radius={self.radius}, resolution={self.resolution})>"

    def process(self, display, size, position):
        surface = pygame.Surface(size)
        surface.blit(display, (0, 0), (position[0], position[1], size[0], size[1]))
        surface = pygame.transform.rotozoom(surface, 0, (self.resolution / 100.0) * 1)
        _size = surface.get_size()
        bytesurf = pygame.image.tostring(surface, "RGBA", False)
        bytesurf = Image.frombytes("RGBA", _size, bytesurf)
        bytesurf = bytesurf.filter(ImageFilter.BoxBlur(radius=int(self.radius)))
        bytesurf = pygame.image.frombuffer(bytesurf.tobytes(), bytesurf.size, bytesurf.mode).convert()
        bytesurf = pygame.transform.rotozoom(bytesurf, 0, (100.0 / self.resolution) * 1)
        display.blit(bytesurf, position)


class MedianFilter:

    def __init__(self, size=3, resolution=40):
        self.size = size
        self.resolution = resolution

    def __repr__(self):
        return f"<heat2d.postprocess.GaussianBlur(size={self.size}, resolution={self.resolution})>"

    def process(self, display, size, position):
        surface = pygame.Surface(size)
        surface.blit(display, (0, 0), (position[0], position[1], size[0], size[1]))
        surface = pygame.transform.rotozoom(surface, 0, (self.resolution / 100.0) * 1)
        _size = surface.get_size()
        bytesurf = pygame.image.tostring(surface, "RGBA", False)
        bytesurf = Image.frombytes("RGBA", _size, bytesurf)
        bytesurf = bytesurf.filter(ImageFilter.MedianFilter(size=int(self.size)))
        bytesurf = pygame.image.frombuffer(bytesurf.tobytes(), bytesurf.size, bytesurf.mode).convert()
        bytesurf = pygame.transform.rotozoom(bytesurf, 0, (100.0 / self.resolution) * 1)
        display.blit(bytesurf, position)


class MinFilter:

    def __init__(self, size=3, resolution=40):
        self.size = size
        self.resolution = resolution

    def __repr__(self):
        return f"<heat2d.postprocess.GaussianBlur(size={self.size}, resolution={self.resolution})>"

    def process(self, display, size, position):
        surface = pygame.Surface(size)
        surface.blit(display, (0, 0), (position[0], position[1], size[0], size[1]))
        surface = pygame.transform.rotozoom(surface, 0, (self.resolution / 100.0) * 1)
        _size = surface.get_size()
        bytesurf = pygame.image.tostring(surface, "RGBA", False)
        bytesurf = Image.frombytes("RGBA", _size, bytesurf)
        bytesurf = bytesurf.filter(ImageFilter.MinFilter(size=int(self.size)))
        bytesurf = pygame.image.frombuffer(bytesurf.tobytes(), bytesurf.size, bytesurf.mode).convert()
        bytesurf = pygame.transform.rotozoom(bytesurf, 0, (100.0 / self.resolution) * 1)
        display.blit(bytesurf, position)


class MaxFilter:

    def __init__(self, size=3, resolution=40):
        self.size = size
        self.resolution = resolution

    def __repr__(self):
        return f"<heat2d.postprocess.GaussianBlur(size={self.size}, resolution={self.resolution})>"

    def process(self, display, size, position):
        surface = pygame.Surface(size)
        surface.blit(display, (0, 0), (position[0], position[1], size[0], size[1]))
        surface = pygame.transform.rotozoom(surface, 0, (self.resolution / 100.0) * 1)
        _size = surface.get_size()
        bytesurf = pygame.image.tostring(surface, "RGBA", False)
        bytesurf = Image.frombytes("RGBA", _size, bytesurf)
        bytesurf = bytesurf.filter(ImageFilter.MaxFilter(size=int(self.size)))
        bytesurf = pygame.image.frombuffer(bytesurf.tobytes(), bytesurf.size, bytesurf.mode).convert()
        bytesurf = pygame.transform.rotozoom(bytesurf, 0, (100.0 / self.resolution) * 1)
        display.blit(bytesurf, position)


class ModeFilter:

    def __init__(self, size=3, resolution=40):
        self.size = size
        self.resolution = resolution

    def __repr__(self):
        return f"<heat2d.postprocess.GaussianBlur(size={self.size}, resolution={self.resolution})>"

    def process(self, display, size, position):
        surface = pygame.Surface(size)
        surface.blit(display, (0, 0), (position[0], position[1], size[0], size[1]))
        surface = pygame.transform.rotozoom(surface, 0, (self.resolution / 100.0) * 1)
        _size = surface.get_size()
        bytesurf = pygame.image.tostring(surface, "RGBA", False)
        bytesurf = Image.frombytes("RGBA", _size, bytesurf)
        bytesurf = bytesurf.filter(ImageFilter.ModeFilter(size=int(self.size)))
        bytesurf = pygame.image.frombuffer(bytesurf.tobytes(), bytesurf.size, bytesurf.mode).convert()
        bytesurf = pygame.transform.rotozoom(bytesurf, 0, (100.0 / self.resolution) * 1)
        display.blit(bytesurf, position)

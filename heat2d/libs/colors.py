GRAYSCALE = "GRAYSCALE"
INVERT = "INVERT"

class RGB:
    @staticmethod
    def to(rgb, type):
        if type == GRAYSCALE: return tuple((rgb[0] + rgb[1] + rgb[2]) // 3 for i in range(3))
        elif type == INVERT: return tuple(255 - c for c in rgb)
        elif type == HEX: return "#%02x%02x%02x" % rgb

class HEX:
    @staticmethod
    def to(hex, type):
        if type == GRAYSCALE: return RGB.to(RGB.to(HEX.to(hex, RGB), GRAYSCALE), HEX)
        if type == INVERT: return RGB.to(RGB.to(HEX.to(hex, RGB), INVERT), HEX)
        if type == RGB: return tuple(int(hex.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))

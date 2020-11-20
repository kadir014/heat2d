import colorsys
from random import choice
from math import sqrt


class Color:
    # r, g, b[, a]
    # (r, g, b[, a])
    # "#hex"
    # "colorname"
    def __init__(self, c, g=None, b=None, a=None):
        if isinstance(c, (int, float)):
            if a:
                self.r, self.g, self.b, self.a = c, g, b, a
            else:
                self.r, self.g, self.b, self.a = c, g, b, 255

        elif isinstance(c, (tuple, list)):
            if len(c) == 4:
                self.r, self.g, self.b, self.a = c
            elif len(c) == 3:
                self.r, self.g, self.b, self.a = c + (255,)

            else:
                raise ValueError("Unexpected elements, length of tuple/list must be 3 (or 4, including alpha)")

        elif isinstance(c, str):
            if c.startswith("#"):
                self.r, self.g, self.b, self.a = tuple(int(h[i:i+2], 16) for i in (0, 2, 4)) + (255,)

            elif c.lower().replace(" ", "").replace("-", "") in colors_dict:
                self.r, self.g, self.b, self.a = colors_dict[c.lower().replace(" ", "").replace("-", "")] + (255,)

            else:
                raise ValueError(f"Color argument {c} is invalid")

        else:
            raise ValueError(f"Color argument {c} is invalid")

        self.__h, self.__s, self.__l = colorsys.rgb_to_hls(self.r/255, self.g/255, self.b/255)

    def __repr__(self):
        return f"<heat2d.Color({self.r}, {self.g}, {self.b}, alpha={self.a})>"

    def to_tuple(self):
        return (self.r, self.g, self.b, self.a)

    def normalise(self):
        return Color(self.r/255, self.g/255, self.b/255)

    def negative(self):
        return Color(255-self.r, 255-self.g, 255-self.b, 255)

    def grayscale(self):
        avg = int((self.r + self.g, + self.b) / 3)
        return Color(avg, avg, avg, 255)

    def distance(self, color):
        return sqrt((self.r - color.r)**2 + (self.g - color.g)**2 + (self.b - color.b)**2)

    def distance2(self, color):
        return (self.r - color.r)**2 + (self.g - color.g)**2 + (self.b - color.b)**2

    @property
    def h(self): return self.__h

    @h.setter
    def h(self, val):
        self.__h = val
        self.r, self.g, self.b = colorsys.hls_to_rgb(self.__h, self.__s, self.__l)
        self.r *= 255
        self.g *= 255
        self.b *= 255

    @property
    def s(self): return self.__s

    @s.setter
    def s(self, val):
        self.__s = val
        self.r, self.g, self.b = colorsys.hls_to_rgb(self.__h, self.__s, self.__l)
        self.r *= 255
        self.g *= 255
        self.b *= 255

    @property
    def l(self): return self.__l

    @l.setter
    def l(self, val):
        self.__l = val
        self.r, self.g, self.b = colorsys.hls_to_rgb(self.__h, self.__s, self.__l)
        self.r *= 255
        self.g *= 255
        self.b *= 255


class Palette:
    def __init__(self, color_list):
        if isinstance(color_list, str):
            self.__color_list = palettes_dict[color_list]
        elif isinstance(color_list, (tuple, list)):
            self.__color_list = color_list
        else:
            raise ValueError("Argument must be str or list/tuple")

    def __repr__(self):
        return f"<heat2d.Palette({len(self.__color_list)} colors)>"

    def __len__(self):
        return len(self.__color_list)

    def __getitem__(self, index):
        return self.__color_list[index]

    def get_random(self):
        return choice(self.__color_list)

    def get_average(self, alpha=255):
        r = 0
        g = 0
        b = 0
        alpha = alpha
        for color in self.__color_list:
            r += color.r
            g += color.g
            b += color.b

        r = int(r/len(self.__color_list))
        g = int(g/len(self.__color_list))
        b = int(b/len(self.__color_list))

        return Color(r, g, b, alpha)


colors_dict = {
                #Red
                "lightsalmon"    : (255, 160, 122),
                "salmon"         : (250, 128, 114),
                "darksalmon"     : (233, 150, 122),
                "lightcoral"     : (240, 128, 128),
                "indianred"      : (205, 92, 92),
                "crimson"        : (220, 20, 60),
                "firebrick"      : (178, 34, 34),
                "red"            : (255, 0, 0),
                "darkred"        : (139, 0, 0),
                "lightred"       : (255, 139, 139),

                #Orange
                "coral"          : (255, 127, 80),
                "tomato"         : (255, 99, 71),
                "orangered"      : (255, 69, 0),
                "gold"           : (255, 215, 0),
                "orange"         : (255, 165, 0),
                "darkorange"     : (230, 127, 2),
                "lightorange"    : (255, 187, 77),

                #Yellow
                "lemonchiffon"    : (255, 255, 224),
                "rodyellow"       : (250, 250, 210),
                "papayawhip"      : (255, 239, 213),
                "moccasin"        : (255, 228, 181),
                "peachpuff"       : (255, 218, 185),
                "palegolden"      : (238, 232, 170),
                "khaki"           : (240, 230, 140),
                "darkkhaki"       : (189, 183, 107),
                "yellow"          : (255, 255, 0),
                "darkyellow"      : (227, 200, 0),
                "lightyellow"     : (255, 255, 224),

                #Green
                "lawngreen"       : (124, 252, 0),
                "lime"            : (0, 255, 0),
                "darklime"        : (50, 205, 50),
                "lightlime"       : (120, 255, 120),
                "greenyellow"     : (173, 255, 47),
                "yellowgreen"     : (154, 205, 50),
                "springgreen"     : (0, 255, 127),
                "palegreen"       : (152, 251, 152),
                "seagreen"        : (46, 139, 87),
                "darkseagreen"    : (143, 188, 143),
                "mediumseagreen"  : (60, 179, 113),
                "lightgseagreen"  : (130, 255, 174),
                "olive"           : (128, 128, 0),
                "darkolive"       : (85, 107, 47),
                "lightolive"      : (181, 191, 67),
                "olivedrab"       : (107, 142, 35),
                "green"           : (0, 128, 0),
                "darkgreen"       : (0, 100, 0),
                "lightgreen"      : (144, 238, 144),

                #Cyan
                "aquamarine"      : (127, 255, 212),
                "darkaquamarine"  : (102, 205, 170),
                "paleturqoise"    : (175, 238, 238),
                "turqoise"        : (64, 224, 208),
                "darkturqoise"    : (60, 181, 169),
                "cadetblue"       : (95, 158, 160),
                "teal"            : (0, 128, 128),
                "aqua"            : (0, 255, 255),
                "cyan"            : (0, 255, 255),
                "lightaqua"       : (224, 255, 255),
                "lightcyan"       : (224, 255, 255),
                "darkaqua"        : (0, 139, 139),
                "darkcyan"        : (0, 139, 139),

                #Blue
                "powderblue"      : (176,224,230),
                "skyblue"         : (135,206,235),
                "lightskyblue"    : (173, 226, 255),
                "deepskyblue"     : (0,191,255),
                "steelblue"       : (70,130,180),
                "lightsteelblue"  : (176,196,222),
                "dodgerblue"      : (30,144,255),
                "comflowerblue"   : (100,149,237),
                "royalblue"       : (65,105,225),
                "mediumblue"      : (0,0,205),
                "navy"            : (0,0,128),
                "midnightblue"    : (25,25,112),
                "blue"            : (0, 0, 255),
                "darkblue"        : (0, 0, 139),
                "lightblue"       : (66, 66, 255),

                #Purple
                "lavender"        : (230,230,250),
                "thistle"         : (216,191,216),
                "plum"            : (221,160,221),
                "violet"          : (238,130,238),
                "orchid"          : (218,112,214),
                "fuchsia"         : (255,0,255),
                "magenta"         : (255,0,255),
                "blueviolet"      : (138,43,226),
                "darkviolet"      : (148,0,211),
                "darkorchid"      : (153,50,204),
                "darkfuchsia"     : (139,0,139),
                "darkmagenta"     : (139,0,139),
                "indigo"          : (75,0,130),
                "purpleblue"      : (123,104,238),
                "darkpurpleblue"  : (78, 49, 173),
                "lightpurpleblue" : (185, 166, 255),
                "purple"          : (128,0,128),
                "darkpurple"      : (82, 6, 99),
                "lightpurple"     : (204, 71, 204),

                #Pink
                "hotpink"         : (255,105,180),
                "deeppink"        : (255,20,147),
                "palevioletred"   : (219,112,147),
                "mediumvioletred" : (199,21,133),
                "pink"            : (255,192,203),
                "darkpink"        : (219, 151, 171),
                "lighpink"        : (255, 227, 232),

                #Brown
                "comsilk"         : (255,248,220),
                "blanchedalmond"  : (255,235,205),
                "bisque"          : (255,228,196),
                "navajowhite"     : (255,222,173),
                "wheat"           : (245,222,179),
                "burlywood"       : (222,184,135),
                "tan"             : (210,180,140),
                "rosybrown"       : (188,143,143),
                "sandybrown"      : (244,164,96),
                "goldenrod"       : (218,165,32),
                "peru"            : (205,133,63),
                "chocolate"       : (210,105,30),
                "saddlebrown"     : (139,69,19),
                "sienna"          : (160,82,45),
                "brownred"        : (165,42,42),
                "maroon"          : (128,0,0),
                "brown"           : (173, 88, 62),
                "darkbrown"       : (92, 36, 19),
                "lightbrown"      : (227, 126, 95),

                #White
                "snow"            : (255,250,250),
                "honeydew"        : (240,255,240),
                "mintcream"       : (245,255,250),
                "azure"           : (240,255,255),
                "aliceblue"       : (240,248,255),
                "ghostwhite"      : (248,248,255),
                "whitesmoke"      : (245,245,245),
                "seashell"        : (255,245,238),
                "beige"           : (245,245,220),
                "oldlace"         : (253,245,230),
                "floralwhite"     : (255,250,240),
                "ivory"           : (255,255,240),
                "antiquewhite"    : (250,235,215),
                "linen"           : (250,240,230),
                "mistyrose"       : (255,228,225),
                "white"           : (255, 255, 255),

                #Gray
                "gainsboro"       : (220,220,220),
                "silver"          : (192,192,192),
                "dimgray"         : (105,105,105),
                "slategray"       : (112,128,144),
                "lightslategray"  : (119,136,153),
                "darkslategray"   : (74, 87, 99),
                "deepgray"        : (38, 38, 38),
                "black"           : (0, 0, 0),
                "lightblack"      : (26, 26, 26),
                "gray"            : (128,128,128),
                "lightgray"       : (211,211,211),
                "darkgray"        : (84, 84, 84)
              }

palettes_dict = {
                  "rainbow" : Palette([
                                       Color("red"),
                                       Color("orange"),
                                       Color("yellow"),
                                       Color("lime"),
                                       Color("blue"),
                                       Color("purple")
                                     ]),

                  "grayscale" : Palette([
                                         Color(255, 255, 255),
                                         Color(230, 230, 230),
                                         Color(205, 205, 205),
                                         Color(180, 180, 180),
                                         Color(155, 155, 155),
                                         Color(130, 130, 130),
                                         Color(105, 105, 105),
                                         Color(80, 80, 80),
                                         Color(55, 55, 55),
                                         Color(30, 30, 30),
                                         Color(0, 0, 0)
                                        ]),

                  "gameboy" : Palette([
                                       Color(202, 220, 159),
                                       Color(155, 188, 15),
                                       Color(139, 172, 15),
                                       Color(48, 98, 48),
                                       Color(15, 65, 15)
                                      ]),
                }

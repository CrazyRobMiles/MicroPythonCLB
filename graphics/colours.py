import random

class Colour:
    def __init__(self, r=0.0, g=0.0, b=0.0):
        self.r = r
        self.g = g
        self.b = b

    def copy(self):
        return Colour(self.r, self.g, self.b)

    def __repr__(self):
        return f"Colour({self.r:.2f}, {self.g:.2f}, {self.b:.2f})"

# Short form named colours
colour_char_lookup = {
    'K': Colour(0, 0, 0),
    'R': Colour(1, 0, 0),
    'G': Colour(0, 1, 0),
    'B': Colour(0, 0, 1),
    'Y': Colour(1, 1, 0),
    'O': Colour(1, 165/255, 0),
    'M': Colour(1, 0, 1),
    'C': Colour(0, 1, 1),
    'W': Colour(1, 1, 1),
    'A': Colour(0, 138/255, 216/255),
    'V': Colour(143/255, 0, 1),
    'P': Colour(128/255, 0, 128/255),
    'T': Colour(0, 128/255, 128/255)
}

# Named colours (subset for brevity)
colour_name_lookup = [
    ("black", Colour(0, 0, 0)),
    ("red", Colour(1, 0, 0)),
    ("green", Colour(0, 1, 0)),
    ("blue", Colour(0, 0, 1)),
    ("yellow", Colour(1, 1, 0)),
    ("orange", Colour(1, 165/255, 0)),
    ("magenta", Colour(1, 0, 1)),
    ("cyan", Colour(0, 1, 1)),
    ("white", Colour(1, 1, 1)),
    ("azure", Colour(0, 138/255, 216/255)),
    ("blueviolet", Colour(138/255, 43/255, 226/255)),
    ("brown", Colour(165/255, 42/255, 42/255)),
    ("chartreuse", Colour(127/255, 255/255, 0)),
    ("darkgreen", Colour(0, 100/255, 0)),
    ("darkmagenta", Colour(139/255, 0, 139/255)),
    ("darkorange", Colour(255/255, 140/255, 0)),
    ("darkred", Colour(139/255, 0, 0)),
    ("darkturquoise", Colour(0, 206/255, 209/255)),
    ("darkviolet", Colour(148/255, 0, 211/255)),
    ("deeppink", Colour(255/255, 20/255, 147/255)),
    ("deepskyblue", Colour(0, 191/255, 255/255)),
    ("firebrick", Colour(178/255, 34/255, 34/255)),
    ("forestgreen", Colour(34/255, 139/255, 34/255)),
    ("gold", Colour(255/255, 215/255, 0)),
    ("indianred", Colour(205/255, 92/255, 92/255)),
    ("lawngreen", Colour(124/255, 252/255, 0)),
    ("lightseagreen", Colour(32/255, 178/255, 170/255)),
    ("limegreen", Colour(50/255, 205/255, 50/255)),
    ("maroon", Colour(128/255, 0, 0)),
    ("mediumblue", Colour(0, 0, 205/255)),
    ("mediumspringgreen", Colour(0, 250/255, 154/255)),
    ("mediumviolet", Colour(199/255, 21/255, 133/255)),
    ("midnightblue", Colour(25/255, 25/255, 112/255)),
    ("navy", Colour(0, 0, 128/255)),
    ("orchid", Colour(218/255, 112/255, 214/255)),
    ("purple", Colour(128/255, 0, 128/255)),
    ("saddlebrown", Colour(139/255, 69/255, 19/255)),
    ("salmon", Colour(250/255, 128/255, 114/255)),
    ("seagreen", Colour(46/255, 139/255, 87/255)),
    ("springgreen", Colour(0, 1, 127/255)),
    ("teal", Colour(0, 128/255, 128/255)),
    ("tomato", Colour(255/255, 99/255, 71/255)),
    ("violet", Colour(143/255, 0, 1))
]


# Lookups

def find_colour_by_name(name):
    for n, c in colour_name_lookup:
        if name.lower() == n:
            return c.copy()
    return None

def find_colour_by_char(ch):
    return colour_char_lookup.get(ch.upper(), None)

def find_random_colour():
    return random.choice(colour_name_lookup[1:])[1].copy()  # skip black

def get_colour_inbetween_mask(low_char, high_char, distance):
    from_col = find_colour_by_char(low_char)
    to_col = find_colour_by_char(high_char)
    if not from_col or not to_col:
        return Colour(0, 0, 0)
    red = from_col.r + (to_col.r - from_col.r) * distance
    green = from_col.g + (to_col.g - from_col.g) * distance
    blue = from_col.b + (to_col.b - from_col.b) * distance
    return Colour(red, green, blue)

BLACK = Colour(0, 0, 0)


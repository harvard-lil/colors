import os

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
DATA_DIR = os.path.join(DIR, 'data')
COLOR_LIST = ["amber", "amethyst", "apricot", "aqua", "aquamarine", "auburn", "azure", "beige", "black", "blue",
              "bronze", "brown", "buff", "carmine", "celadon", "cerise", "cerulean", "charcoal", "chartreuse",
              "chocolate", "cinnamon", "copper", "coral", "cream", "crimson", "cyan", "denim", "sand", "ebony", "ecru",
              "eggplant", "emerald", "fuchsia", "gold", "goldenrod", "gray", "green", "grey", "indigo", "ivory", "jade",
              "jet", "khaki", "lavender", "lemon", "lilac", "lime", "magenta", "mahogany", "maroon", "mauve", "mustard",
              "navy", "ocher", "olive", "orange", "orchid", "pale", "pastel", "peach", "periwinkle", "persimmon",
              "pewter", "pink", "puce", "pumpkin", "purple", "rainbow", "red", "rose", "ruby", "russet", "rust",
              "saffron", "salmon", "sapphire", "scarlet", "sepia", "shamrock", "sienna", "silver", "slate", "steel",
              "tan", "tangerine", "taupe", "teal", "terracotta", "thistle", "tint", "tomato", "topaz", "turquoise",
              "ultramarine", "umber", "vermilion", "violet", "viridian", "wheat", "white", "wisteria", "yellow"]

SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/colors'

SQLALCHEMY_TRACK_MODIFICATIONS = False

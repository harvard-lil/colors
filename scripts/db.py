import os
import json
from datetime import datetime
import math
import colorsys

from color.trained import get_color

from app import db as database, Color
from config import settings

color_results_file = os.path.join(settings.DATA_DIR, "color_results_copy.txt")


def get_color_words_in_captured_text(text):
    all_words = text.lower().split()
    all_colors = []
    for word in all_words:
        if word in settings.COLOR_LIST:
            all_colors.append(word)
    return all_colors


def parse_date(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d').date()


def init_db():
    database.create_all()


def populate_db():
    with open(color_results_file, "r") as f:
        lines = f.read().split("\n")
    # colors = []
    session = database.create_scoped_session()
    for idx, line in enumerate(lines):
        if not line:
            continue
        res = json.loads(line)

        try:
            color = Color(idx)
            color.case_id = res["id"]
            color.name_abbreviation = res["name_abbreviation"]
            color.context = res["context"]
            color.captured_text = res["captured_text"]
            color.date = parse_date(res["date"])
            session.add(color)
            session.commit()
        except Exception as e:
            print("caught error")
            pass

    print("done!!")


def lum(r, g, b):
    return math.sqrt(.241 * r + .691 * g + .068 * b)


def populate_colors_in_db():
    session = database.create_scoped_session()
    colors = Color.query.all()
    for color in colors:
        color_obj = get_color(color.captured_text)

        original_rgb_vals = [float(item) for item in color_obj["rgb"]]

        color.rgb = [int(item) for item in original_rgb_vals]
        color.lab = [float(item) for item in color_obj["lab"]]
        color.hex = color_obj["hex"][1:]
        color.lum = lum(*original_rgb_vals)
        color.hsv = list(colorsys.rgb_to_hsv(*color.rgb))
        session.merge(color)
        session.flush()
        session.commit()
        print("added", color.id)

# TODO!
def remove_names_in_db():
    session = database.create_scoped_session()
    colors = Color.query.all()
    for color in colors:
        words = color.captured_text.split(' ')
        if '-' in color.captured_text:
            pass
        elif len(words) == 1 and color.captured_text[0] == color.captured_text[0].upper():
            session.delete(color)
            session.commit()

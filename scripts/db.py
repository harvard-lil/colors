import os
import json
from datetime import datetime
import math
import colorsys
from contextlib import contextmanager
from multiprocessing.dummy import Pool as ThreadPool
from tqdm import tqdm

from color.trained import get_color

from app import db as database, Color
from config import settings

color_results_file = os.path.join(settings.DATA_DIR, "color_results.txt")


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
    print("Adding colors...")
    with open(color_results_file, "r") as f:
        lines = f.read().split("\n")
    session = database.create_scoped_session()
    # this appears to be faster inline than parallel
    for tup in enumerate(tqdm(lines)):
        add_color(session, tup)
    # work_parallel(add_color, list(enumerate(lines)))
    # and much faster if we commit at the end...
    session.commit()
    print("Done.")


def add_color(session, tup):
    try:
        (idx, line) = tup
        res = json.loads(line)
        color = Color(idx)
        color.case_id = res["id"]
        color.name_abbreviation = res["name_abbreviation"]
        color.context = res["context"]
        color.captured_text = res["captured_text"]
        color.date = parse_date(res["date"])
        session.add(color)
    except Exception as e:
        pass


def lum(r, g, b):
    return math.sqrt(.241 * r + .691 * g + .068 * b)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = database.create_scoped_session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def add_color_data(session, color):
    if color.hex:
        return
    else:
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


def thread_worker(f, x):
    with session_scope() as session:
        f(session, x)
    return 0


def work_parallel(f, xs, thread_number=4):
    pool = ThreadPool(thread_number)
    pbar = tqdm(total=len(list(xs)))
    for x in xs:
        pool.apply_async(thread_worker, (f, x), callback=lambda a: pbar.update())
    pool.close()
    pool.join()
    pbar.close()


def populate_colors_in_db():
    print("Adding color data...")
    session = database.create_scoped_session()
    colors = session.query(Color)
    work_parallel(add_color_data, colors)


# TODO!
def remove_names_in_db():
    session = database.create_scoped_session()
    colors = session.query(Color)
    for color in colors:
        words = color.captured_text.split(' ')
        if '-' in color.captured_text:
            pass
        elif len(words) == 1 and color.captured_text[0] == color.captured_text[0].upper():
            session.delete(color)
    session.commit()

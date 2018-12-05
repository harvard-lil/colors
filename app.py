import os
import json

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import settings
from flask import request, render_template
from flask import jsonify

from color.trained import get_color


app = Flask(__name__, static_url_path='/static')
app.config.from_pyfile(os.path.join(settings.DIR, 'config/settings.py'))
db = SQLAlchemy(app)
migrate = Migrate(app, db)

color_computed_file = os.path.join(settings.DATA_DIR, "computed_color_results.json")


# FLASK_APP=web/app.py FLASK_DEBUG=1 python -m flask run


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template("main.html")
    elif request.method == 'POST':
        color_string = request.form.get('color', None)

        if not color_string:
            return render_template("main.html")

        hex_color = get_color(color_string)['hex']
        return render_template("main.html", color_string=color_string, color=hex_color)


@app.route("/color", methods=['GET'])
def color():
    color_string = request.args.get("name", None)
    if not color_string:
        return jsonify({"color": None, "status": 204, "value": color_string})

    color_obj = get_color(color_string)

    return jsonify({"hex": color_obj['hex'],
                    "rgb": color_obj['rgb'],
                    "lab": color_obj['lab'],
                    "status": 200,
                    "value": color_string})


@app.route("/show", methods=['GET'])
def show_hex():
    with open(color_computed_file, "r") as f:
        results = json.load(f)
        return render_template("cases.html", results=results)


@app.route("/hsv", methods=["GET"])
def show_hsv():
    import colorsys
    with open(color_computed_file, "r") as f:
        color_results = json.load(f)

    # hsv sort
    for c in color_results:
        c["color_rgb"] = list(map(lambda x: float(x), c["color_rgb"]))
        c["color_lab"] = list(map(lambda x: float(x), c["color_lab"]))
    color_results.sort(key=lambda item: colorsys.rgb_to_hsv(*item["color_rgb"]))
    return render_template("cases.html", results=color_results)


@app.route("/hsl", methods=["GET"])
def show_hsl():
    import colorsys
    with open(color_computed_file, "r") as f:
        color_results = json.load(f)

    # hsv sort
    for c in color_results:
        c["color_rgb"] = list(map(lambda x: float(x), c["color_rgb"]))
        c["color_lab"] = list(map(lambda x: float(x), c["color_lab"]))
    color_results.sort(key=lambda item: colorsys.rgb_to_hls(*item["color_rgb"]))
    return render_template("cases.html", results=color_results)


@app.route("/lum", methods=["GET"])
def show_lum():
    import math
    with open(color_computed_file, "r") as f:
        color_results = json.load(f)

    # hsv sort
    for c in color_results:
        c["color_rgb"] = list(map(lambda x: float(x), c["color_rgb"]))
        c["color_lab"] = list(map(lambda x: float(x), c["color_lab"]))

    def lum(r, g, b):
        return math.sqrt(.241 * r + .691 * g + .068 * b)

    color_results.sort(key=lambda item: lum(*item["color_rgb"]))
    return render_template("cases.html", results=color_results)


@app.route("/date", methods=["GET"])
def show_date():
    starting_num = 5000
    increment = 1000
    page = request.args.get("page", None)
    if page:
        from_data = starting_num + (int(page)*increment)
        to_data = from_data+increment
        print("from data:", from_data, "to data:", to_data)
        colors = Color.query.order_by("id").all()[from_data:to_data]
        # if len(colors):
        colors_to_send = [color.as_dict() for color in colors]
        return jsonify(colors_to_send)
    else:
        # db.create_scoped_session()
        colors = Color.query.order_by("id").limit(starting_num).all()
        return render_template("cases.html", results=colors)


class Color(db.Model):
    __tablename__ = "colors"
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer)
    date = db.Column(db.Date)
    name_abbreviation = db.Column(db.String(200))
    captured_text = db.Column(db.String(800))
    context = db.Column(db.String(2000))
    hex = db.Column(db.String(20))
    rgb = db.Column(db.ARRAY(db.Integer))
    lab = db.Column(db.ARRAY(db.Integer))
    hsv = db.Column(db.ARRAY(db.Integer))
    lum = db.Column(db.Float)

    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return '<id %r>' % self.id

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}


if __name__ == '__main__':
    app.debug = True
    app.run()

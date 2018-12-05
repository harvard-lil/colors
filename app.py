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


@app.route("/date", methods=["GET"])
def show_date():
    page = request.args.get("page", None)
    if page:
        colors_to_send = request_incremental(order="id", page=page)
        return jsonify(colors_to_send)
    else:
        # db.create_scoped_session()
        colors = Color.query.order_by("id").limit(5000).all()
        return render_template("cases.html", results=colors)


@app.route("/lum", methods=["GET"])
def show_lum():
    page = request.args.get("page", None)
    if page:
        colors_to_send = request_incremental(order="lum", page=page)
        return jsonify(colors_to_send)
    else:
        # db.create_scoped_session()
        colors = Color.query.order_by("lum").all()

        return render_template("cases.html", results=colors[0:5000])


def request_incremental(order="lum", page=0):
    starting_num = 5000
    increment = 1000
    from_data = starting_num + (int(page) * increment)
    to_data = from_data + increment
    colors = Color.query.order_by(order).all()[from_data:to_data]
    return [color.as_dict() for color in colors]


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

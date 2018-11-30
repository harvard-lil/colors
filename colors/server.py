from flask import Flask, request, render_template
from color.trained import get_color
from flask import jsonify
import json

app = Flask(__name__)


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
    with open("/Users/aaizman/Documents/cap-examples/colors/computed_color_results.json", "r") as f:
        results = json.load(f)
        return render_template("cases.html", results=results)


@app.route("/hsv", methods=["GET"])
def show_hsv():
    import colorsys
    with open("/Users/aaizman/Documents/cap-examples/colors/computed_color_results.json", "r") as f:
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
    with open("/Users/aaizman/Documents/cap-examples/colors/computed_color_results.json", "r") as f:
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
    with open("/Users/aaizman/Documents/cap-examples/colors/computed_color_results.json", "r") as f:
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
    with open("/Users/aaizman/Documents/cap-examples/colors/computed_color_results.json", "r") as f:
        color_results = json.load(f)
    return render_template("cases.html", results=color_results)


if __name__ == '__main__':
    app.run()

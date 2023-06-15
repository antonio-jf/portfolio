from flask import Flask, render_template, request, redirect, Response
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from cs50 import SQL
import statistics

app = Flask(__name__)
db = SQL("sqlite:///bycicle.db")

VARS = ["Rideable type", "Start station", "Start station ID",
        "End station", "End station ID", "Member type"]
VALS = ["rideable_type", "start_station_name", "start_station_id", "end_station_name", "end_station_id", "member_casual"]
STATS = ["Average", "Median"]

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/data_structure')
def data_structure():
    return render_template("data_structure.html")


@app.route("/about")
def about():
    return render_template("about.html")


def plot_data(data, val, stat):
    x = []
    for dat in data:
        if len(dat[val]) > 20:
            x.append(dat[val][0:19])
        else:
            x.append(dat[val])

    y = [dat['cnt'] for dat in data]

    plt.gca().cla()
    plt.bar(x, y)
    plt.xticks(rotation=90)  # Rotates X-Axis Ticks by 45-degrees
    if stat == "Average":
        plt.axhline(y = statistics.mean(y), color = 'r', linestyle = '-')
    else:
        plt.axhline(y = statistics.median(y), color='r', linestyle='-')
    plt.suptitle(f"Red line indicates {stat}")
    plt.title(f"Top results for {val}")
    plt.subplots_adjust(bottom=0.40)
    return plt


def get_rows(val):

    rows = db.execute(f"SELECT DISTINCT {val}, COUNT({val}) AS cnt FROM 'tripdata-apr-2023' GROUP BY {val} ORDER BY cnt DESC LIMIT 50")
    query = f"SELECT DISTINCT {val}, COUNT({val}) AS cnt FROM 'tripdata-apr-2023' GROUP BY {val} ORDER BY cnt DESC LIMIT 50"
    return rows, query


@app.route("/query", methods=["GET", "POST"])
def query():
    if request.method == "GET":
        return render_template("query.html", vars=list(zip(VALS, VARS)), stats=STATS)
    else:
        val = str(request.form.get("var"))
        stat = request.form.get("stat")

        data, quer = get_rows(val)
        plot_data(data, val, stat)
        path = os.path.join('static', 'images', 'plot.png')
        plt.savefig(path)

        return render_template("results.html", query=quer)


@app.route("/results")
def results():
    return render_template("results.html")




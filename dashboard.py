from bokeh.models import ColumnDataSource
from bokeh.layouts import gridplot
from bokeh.embed import components
from bokeh.plotting import figure, output_file, show
from bokeh.resources import INLINE
import pickle
import numpy as np
import pandas as pd
import json
import datetime

from flask import Flask, render_template

testfile = "1608669595.842317"

app = Flask(__name__)


@app.route("/")
def index():
    data = []
    with open("data/newstest2", "r") as infile:
        for line in infile:
            data.append(json.loads(line))
    comments = []
    analyses = []
    for line in data:
        comments.append(line["comment"])
        analyses.append(line["analysis"][0])

    df = pd.DataFrame.from_dict(comments)
    df["analysis"] = analyses
    df.sort_values(by="created_utc", ascending=True)
    df["created_datetime"] = df["created_utc"].apply(datetime.datetime.fromtimestamp)
    df.sort_values(by="created_datetime")

    df = df.set_index("created_datetime")

    rolling = df.rolling("10s", min_periods=1)

    sentiment_mean = rolling["analysis"].mean()
    sentiment_std = rolling["analysis"].std()
    datetimes = sentiment_mean.index

    p = figure(
        title="Sentiment Tracker",
        x_axis_label="Datetime",
        y_axis_label="Sentiment",
        x_axis_type="datetime",
    )

    p.line(datetimes, sentiment_mean)

    p.line(datetimes, sentiment_mean + sentiment_std, line_color="red")
    p.line(datetimes, sentiment_mean - sentiment_std, line_color="red")

    p.varea(
        x=datetimes,
        y1=sentiment_mean - sentiment_std,
        y2=sentiment_mean + sentiment_std,
        fill_color="red",
        fill_alpha=0.2,
    )

    script, div = components(p)

    return render_template(
        "index.html",
        plot_script=script,
        plot_div=div,
        js_resources=INLINE.render_js(),
        css_resources=INLINE.render_css(),
    ).encode(encoding="UTF-8")


if __name__ == "__main__":
    app.run(debug=True)

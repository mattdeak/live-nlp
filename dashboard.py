from bokeh.models import ColumnDataSource
from bokeh.layouts import gridplot
from bokeh.embed import components
from bokeh.plotting import figure, output_file, show
from bokeh.resources import INLINE
import pickle
import numpy as np
import pandas as pd

from flask import Flask, render_template

testfile = "1608669595.842317"

app = Flask(__name__)

@app.route("/")
def index():
    with open(testfile, "rb") as infile:
        data = pickle.load(infile)

    comments, sentiment = data
    chart_data = {"text": comments, "sentiment": sentiment.reshape(-1)}

    p = figure(
        title="Sentiment Histogram", x_axis_label="Sentiment", y_axis_label="Count"
    )

    hist, edges = np.histogram(chart_data["sentiment"], bins=20)
    p.quad(
        top=hist,
        bottom=0,
        left=edges[:-1],
        right=edges[1:],
        fill_color="navy",
        line_color="white",
        alpha=0.5,
    )

    script, div = components(p)

    return render_template(
            'index.html',
            plot_script=script,
            plot_div=div,
            js_resources=INLINE.render_js(),
            css_resources=INLINE.render_css()).encode(encoding='UTF-8')


if __name__ == "__main__":
    app.run(debug=True)


from bokeh.embed import server_document
from bokeh.client import pull_session
from bokeh.plotting import figure, output_file, show
from bokeh.resources import INLINE
import pickle
import numpy as np
import pandas as pd
import json
import datetime

from flask import Flask, render_template

testfile = "1608669595.842317"
default_url = 'http://0.0.0.0:5006/streaming_chart'

app = Flask(__name__)


@app.route("/")
def index():

    script = server_document(default_url)

    return render_template(
        "index.html",
        plot_script=script,
        template='Flask'
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

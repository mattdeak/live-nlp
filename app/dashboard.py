from bokeh.embed import server_document
from bokeh.client import pull_session
from bokeh.plotting import figure, output_file, show
from bokeh.resources import INLINE
import pickle
import numpy as np
import pandas as pd
import json
import datetime

from flask import Flask, render_template, request, redirect, url_for

default_url = "http://0.0.0.0:5006/streaming_chart"
app = Flask(__name__)


@app.route("/")
def index():
    script = server_document(default_url)

    return render_template(
        "index.html", plot_script=script, plot_title="default", template="Flask"
    )


@app.route("/reddit/<subreddit>")
def reddit_query(subreddit):
    script = server_document(default_url)

    return render_template(
        "index.html",
        plot_script=script,
        plot_title=f'Reddit Query: {subreddit}',
        template="Flask",
    )

@app.route("/refresh_bot", methods=['POST', 'GET'])
def refresh_bot():
    if request.method == 'GET':
        return f"URL /refresh_bot should not be accessed directly"
    elif request.method == 'POST':
        form_data = request.form
        source = form_data['sources']
        if source != 'reddit':
            return f'Source : {source} not yet supported'
        else:
            query = form_data['query']
            # TODO: Start another bot and switch the bokeh server somehow.
            return redirect(url_for('reddit_query', subreddit=query))

            




if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

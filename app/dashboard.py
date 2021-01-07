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
from utils import convert_form_to_bot_request, request_new_bot, get_botlist, delete_bot

default_bokeh_url = "http://0.0.0.0:5006/sentiment_streaming"

app = Flask(__name__)


@app.route("/")
def index():
    script = server_document(default_bokeh_url)

    # return render_template(
    #     "index.html", plot_script=script, plot_title="default", template="Flask"
    # )
    return render_template(
        "index.html", plot_title="default", template="Flask"
    )


@app.route("/reddit/<subreddit>")
def reddit_query(subreddit):
    # TODO: Better hash scheme than this. What if a coll has multiple subreddits?
    db_collection = subreddit
    script = server_document(default_bokeh_url, arguments={"collection": subreddit})

    return render_template(
        "index.html",
        plot_script=script,
        plot_title=f"Reddit Query: {subreddit}",
        template="Flask",
    )


@app.route("/refresh_bot", methods=["POST", "GET"])
def refresh_bot():
    if request.method == "GET":
        return f"URL /refresh_bot should not be accessed directly"
    elif request.method == "POST":
        form_data = request.form
        source = form_data["source"]
        if source != "reddit":
            return f"Source : {source} not yet supported"
        else:
            botserver_url, botserver_request = convert_form_to_bot_request(form_data)
            resp = request_new_bot(botserver_url, botserver_request)
            if resp.status_code in [200, 201]:
                query = form_data["query"]
                return redirect(url_for("reddit_query", subreddit=query))
            else:
                return f"Error starting Bot on Botserver: {resp.status_code},{resp.json()}"

@app.route("/view/<collection>")
def view_data(collection):
    return redirect(url_for("reddit_query", subreddit=collection))


@app.route("/refresh_botlist")
def refresh_botlist():
    response = get_botlist()
    return response.json()

@app.route("/delete_bot/<bot_id>", methods=['DELETE'])
def send_deletion_request(bot_id):
    resp = delete_bot(bot_id)
    return str(resp.status_code)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

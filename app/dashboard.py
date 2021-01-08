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

@app.route("/bots")
def bots():
    return render_template("bots.html", template="Flask")

@app.route("/live-analysis", methods=['GET','POST'])
def live():
    # This whole thing is gross. TODO: Make less gross

    chart_list_resp = get_botlist() #TODO: Eventually this should be decoupled from bots
    chart_list = chart_list_resp.json()

    chart_sources = [c.split('|')[-1] for c in chart_list.values()]

    if request.method == 'GET':
        return render_template("charts.html", chart_sources=chart_sources, template="Flask")
    else:
        selected_chart = request.form['chart_source']
        print('selected chart = ' + selected_chart)
        plot_script = server_document(default_bokeh_url, arguments={"collection": selected_chart})
        return render_template("charts.html", chart_sources=chart_sources, plot_script=plot_script, template='Flask')


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
            return redirect(url_for('index'))

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

def list_available_collections():
    pass

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

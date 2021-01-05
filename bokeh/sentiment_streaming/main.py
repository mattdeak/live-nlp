import datetime
import json
from functools import partial
from threading import Thread
import time

import pandas as pd
from bokeh.layouts import column
from bokeh.models import Button
from bokeh.models.sources import ColumnDataSource
from bokeh.plotting import curdoc, figure
from tornado import gen

from .readers import MongoReader
import os

DB_NAME = os.environ["DB_NAME"]

# Session Args
args = curdoc().session_context.request.arguments
collection = str(args["collection"][0])

reader = MongoReader(DB_NAME, collection)


def get_updated_df(last_utc=0):
    data = reader.run(last_utc)

    df = pd.DataFrame.from_dict(data)
    return df


def get_sentiment_stats(df):
    assert df.size > 0, "Dataframe Empty"
    df["created_datetime"] = df["created_utc"].apply(datetime.datetime.fromtimestamp)

    df = df.set_index("created_datetime")
    df = df.sort_index()

    rolling = df.rolling("20s", min_periods=1)

    sentiment_mean = rolling["analysis"].mean()
    sentiment_std = rolling["analysis"].std()
    datetimes = sentiment_mean.index

    return sentiment_mean, sentiment_std, datetimes


# ---- Define Initial Chart ---- #
new_df = get_updated_df()
if new_df.empty:
    most_recent_utc = 0
    new_data = {"x": [], "y": [], "y1": [], "y2": []}
else:
    most_recent_utc = new_df["created_utc"].max()
    new_means, new_stds, new_datetimes = get_sentiment_stats(new_df)

    new_data = {
        "x": new_datetimes,
        "y": new_means,
        "y1": new_means - new_stds,
        "y2": new_means + new_stds,
    }

source = ColumnDataSource(data=new_data)
doc = curdoc()

p = figure(
    name="sentiment_tracker",
    title="Sentiment Tracker",
    x_axis_label="Datetime",
    y_axis_label="Sentiment",
    x_axis_type="datetime",
    y_range=(0, 1),
)

mean = p.line(x="x", y="y", source=source)
fill = p.varea(x="x", y1="y1", y2="y2", fill_color="red", fill_alpha=0.2, source=source)
# ---- Done Chart Definition ---- #


@gen.coroutine
def update(x, y, y1, y2):
    source.stream(dict(x=x, y=y, y1=y1, y2=y2))


def load_new_comments():
    # I don't love this, but it works.
    global most_recent_utc

    while True:
        # Sleep for 3 second
        # TODO: Maybe environ variable? Thnk about it
        time.sleep(3)
        new_df = get_updated_df(last_utc=most_recent_utc)

        # If there were no results, wait til next loop
        if new_df.empty:
            continue

        most_recent_utc = new_df["created_utc"].max()

        new_means, new_stds, new_datetimes = get_sentiment_stats(new_df)

        doc.add_next_tick_callback(
            partial(
                update,
                x=new_datetimes,
                y=new_means,
                y1=new_means - new_stds,
                y2=new_means + new_stds,
            )
        )


doc.add_root(p)
update_thread = Thread(target=load_new_comments)
update_thread.start()

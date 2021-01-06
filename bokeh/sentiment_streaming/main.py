import datetime
import json
import logging
import os
import sys
import time
from functools import partial
from threading import Thread

import pandas as pd
import numpy as np
from bokeh.layouts import column
from bokeh.models import Button
from bokeh.models.sources import ColumnDataSource
from bokeh.plotting import curdoc, figure
from tornado import gen

from .readers import MongoReader

# DB_HOST = os.environ.get("DB_HOST", "localhost")
# DB_PORT = int(os.environ.get("DB_PORT", 27017))
DB_NAME = os.environ["DB_NAME"]
WINDOW_SIZE = os.environ.get("STREAMING_WINDOW_SIZE", 20)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stderr)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    "%(created)f:%(levelname)s:%(name)s:%(module)s:%(message)s"
)
handler.setFormatter(formatter)
logger.addHandler(handler)

# Session Args
args = curdoc().session_context.request.arguments
collection = (args["collection"][0]).decode("utf-8")
logger.info(f"Using Collection: {collection}")

# logger.debug(f'{DB_HOST},{DB_PORT}{DB_NAME}{collection}')
# reader = MongoReader(DB_NAME, collection, host=DB_NAME, port=DB_PORT)
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
    # new_datetimes = new_datetimes.apply(lambda x: np.datetime64('NaT') if x == np.nan else x)
    

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

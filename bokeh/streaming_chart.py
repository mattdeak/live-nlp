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

from readers import MongoReader
import os

DB_NAME = os.environ["DB_NAME"]
COLL_NAME = os.environ["DB_COL"]

reader = MongoReader(DB_NAME, COLL_NAME)


def get_sentiment_stats(last_datetime=0):

    data = reader.read(last_datetime)

    df = pd.DataFrame.from_dict(data)
    df["created_datetime"] = df["created_utc"].apply(datetime.datetime.fromtimestamp)

    df = df.set_index("created_datetime")
    df = df.sort_index()

    rolling = df.rolling("20s", min_periods=1)

    sentiment_mean = rolling["analysis"].mean()
    sentiment_std = rolling["analysis"].std()
    datetimes = sentiment_mean.index

    return sentiment_mean, sentiment_std, datetimes


# ---- Define Initial Chart --- #
new_means, new_stds, new_datetimes = get_sentiment_stats()

new_mean_data = dict()
new_fill_data = dict()

new_mean_data["x"] = new_datetimes
new_mean_data["y"] = new_means
new_fill_data["x"] = new_datetimes
new_fill_data["y1"] = new_means - new_stds
new_fill_data["y2"] = new_means + new_stds

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


@gen.coroutine
def update(x, y, y1, y2):
    source.stream(dict(x=x, y=y, y1=y1, y2=y2))


def load_new_comments():
    while True:
        # Sleep for 3 second
        # TODO: Maybe environ variable? Thnk about it
        time.sleep(3)

        latest_datetime = source.data["x"][-1]
        new_means, new_stds, new_datetimes = get_sentiment_stats()

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

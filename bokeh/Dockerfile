
FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install -y python-pip python-dev build-essential

RUN pip install flask bokeh pymongo pandas

WORKDIR /home/app
COPY . .
# TODO: Don't hardcode port maybe?
CMD bokeh serve streaming_chart.py --allow-websocket-origin=localhost:5000


# FROM python:18.04
FROM python:3.8-buster

# RUN apt-get update && \
#     apt-get install -y python-pip python-dev build-essential

RUN pip install bokeh pandas pymongo

WORKDIR /home/app
# TODO: Don't hardcode port maybe?
CMD ["bokeh","serve","sentiment_streaming", "--allow-websocket-origin=localhost:5000"]

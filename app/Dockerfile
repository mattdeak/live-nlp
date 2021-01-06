FROM python:3.8-buster

# RUN apt-get update && \
#     apt-get install -y python-pip python-dev build-essential

RUN pip install flask bokeh pymongo pandas requests

WORKDIR /home/app
# COPY . .
# TODO: Don't hardcode port maybe?

ENTRYPOINT ["python3"]
CMD ["dashboard.py"]

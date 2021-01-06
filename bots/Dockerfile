
# FROM ubuntu:18.04
FROM python:3.8-buster

# RUN apt-get update && \
#     apt-get install -y python-pip python-dev build-essential

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /home/app
CMD ["python3","botserver.py"]

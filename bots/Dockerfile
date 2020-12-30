FROM tensorflow/tensorflow:latest-gpu-py3


WORKDIR /home/app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD python start_bots.py
        



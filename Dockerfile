FROM python:3.7.1

WORKDIR /root/myapp

COPY requirements.txt *.py ./
COPY modules ./
COPY resources ./

RUN pip install -r requirements.txt

CMD python -u /root/myapp/app.py

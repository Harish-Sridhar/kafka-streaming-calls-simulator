FROM python:3.7.1

WORKDIR /root/myapp

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY *.py ./
RUN mkdir -p modules resources
COPY modules ./modules/
COPY resources ./resources/

CMD python -u /root/myapp/app.py

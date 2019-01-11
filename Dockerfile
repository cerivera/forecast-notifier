FROM python:3.7.2

WORKDIR /opt/app
COPY . /opt/app

RUN pip3 install -r requirements.txt

CMD ["python3", "./main.py"]

FROM python:3.7.7-alpine3.11

RUN apk add sudo
ENV FLASK_APP manange.py
ENV FLASK_CONFIG docker

RUN adduser -D oba
# USER root

RUN mkdir home/oba-python-api

WORKDIR /home/oba-python-api

COPY requirements.txt requirements.txt
RUN python -m venv venv 

RUN apk add postgresql-dev
RUN pip install -r requirements.txt
USER oba


COPY app app
COPY .env .env
COPY migrations migrations
COPY manage.py config.py boot.sh ./

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]

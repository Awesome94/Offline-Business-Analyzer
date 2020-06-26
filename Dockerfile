FROM python:3.7.7

RUN apt-get update && apt-get install -y sudo
# RUN apk add postgresql-dev
ENV FLASK_APP manange.py
ENV FLASK_CONFIG docker

# RUN adduser -D oba
# USER root

RUN mkdir home/oba-python-api

WORKDIR /home/oba-python-api

COPY requirements.txt requirements.txt
RUN python -m venv venv 


RUN pip install -r requirements.txt
# USER oba


COPY app app
COPY .env .env
COPY migrations migrations
COPY manage.py config.py boot.sh ./

RUN chmod +x boot.sh

EXPOSE 5000
CMD ["./boot.sh"]

FROM python:3.7.7

RUN apt-get update && apt-get install -y sudo

ENV FLASK_APP run.py
ENV FLASK_CONFIG docker

RUN mkdir home/oba-python-api

WORKDIR /home/oba-python-api

COPY requirements.txt requirements.txt
RUN python -m venv venv 

RUN pip install -r requirements.txt

COPY app app
COPY .env .env
COPY migrations migrations
COPY run.py config.py boot.sh ./

RUN chmod +x boot.sh

EXPOSE 5000
CMD ["./boot.sh"]

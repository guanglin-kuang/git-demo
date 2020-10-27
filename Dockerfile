FROM python:3.8

COPY requirements.txt /requirements.txt
COPY ./scraping /project
WORKDIR /project

RUN pip install -r /requirements.txt && rm -rf /tmp/*

FROM python:3.10

ENV PYTHONWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY reqirements.txt /app/requiremennts.txt

RUN pip install -r  /app/requiremennts.txt

COPY . .


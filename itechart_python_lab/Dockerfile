# pull official base image
FROM python:3.10.1-slim
# set work directory
WORKDIR /usr/src/app
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# install dependencies
COPY ./requirements.txt .
RUN pip install --upgrade pip \
&& apt-get update \
&& apt-get -y install libpq-dev gcc \
&& pip install -r requirements.txt
# copy project
COPY . .

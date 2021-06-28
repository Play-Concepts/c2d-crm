# https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker
# https://github.com/WinnerOK/uvicorn-gunicorn-fastapi-docker

FROM winnerokay/uvicorn-gunicorn-fastapi:python3.9-slim

# set environment variables
ENV PYTHONWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

# set working directory
#WORKDIR /code

# copy dependencies
COPY requirements.txt ./

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copy project
COPY ./app /app

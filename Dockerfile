# https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker
# https://github.com/WinnerOK/uvicorn-gunicorn-fastapi-docker

FROM tiangolo/uvicorn-gunicorn:python3.8-slim

COPY requirements.txt .
RUN pip install -r requirements.txt

USER 1000

COPY app app

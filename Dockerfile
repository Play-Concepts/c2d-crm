# https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker
# https://github.com/WinnerOK/uvicorn-gunicorn-fastapi-docker

FROM winnerokay/uvicorn-gunicorn-fastapi:python3.9-slim

COPY requirements.txt .
RUN pip install -r requirements.txt

USER 1000

COPY ./app /app

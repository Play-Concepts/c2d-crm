FROM python:3.9-slim

COPY requirements.txt .
RUN pip install -r requirements.txt

USER 1000

COPY app app

CMD ["uvicorn", "app.main:app", "--host", "${HOST:-0.0.0.0}", "--port", "${PORT:-80}"]

FROM python:3.9-slim

COPY requirements.txt entrypoint.sh /
RUN pip install -r requirements.txt

USER 1000
COPY app app

ENTRYPOINT ["/entrypoint.sh"]
CMD ["start"]

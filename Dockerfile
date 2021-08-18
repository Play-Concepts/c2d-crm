FROM python:3.9-slim

ARG stage
ENV STAGE=$stage

COPY requirements*.txt entrypoint.sh /
RUN pip install -r requirements.txt
RUN if [ "${STAGE}" = "dev" ]; then pip install -r requirements-dev.txt; fi

USER 1000
COPY app app

ENTRYPOINT ["/entrypoint.sh"]
CMD ["start"]

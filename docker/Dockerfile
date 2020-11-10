FROM registry.lil.tools/library/python:3.7-buster
ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_SRC=/usr/local/src

RUN apt-get update && apt-get install -y nano postgresql-client

WORKDIR /app

# pip
COPY requirements.txt /app/
RUN pip install pip==19.3.1 \
    && pip install -r requirements.txt \
    && rm requirements.txt

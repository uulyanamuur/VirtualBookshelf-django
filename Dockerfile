FROM python:3.8-slim

ENV  \
    #python
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PYTHONDONTWRITEBYTECODE=1 \
    #poetry
    POETRY_VIRTUALENVS_CREATE=true \
    POETRY_VERSION=1.1.4

RUN apt-get update \
    && apt-get install -y dos2unix \
    && apt-get install netcat -y \
    && apt-get install build-essential python3.8-dev -y \
    && python -m pip install --upgrade pip \
    && pip install "poetry==$POETRY_VERSION" \
    && poetry config virtualenvs.in-project true

WORKDIR /bookshelf
COPY ./docker /docker
COPY ./poetry.lock ./pyproject.toml /bookshelf/

RUN poetry install --no-dev

RUN chmod +x /docker/*

RUN dos2unix /docker/entrypoint.sh && apt-get --purge remove -y dos2unix && rm -rf /var/lib/apt/lists/*
RUN useradd -ms /bin/bash bsuser
USER bsuser
CMD ["bash", "/docker/entrypoint.sh"]

COPY . /bookshelf
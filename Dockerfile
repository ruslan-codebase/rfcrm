FROM python:3.10
LABEL authors="ruslan"

RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python

ENV PATH="${PATH}:/root/.local/bin"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN poetry config virtualenvs.in-project true
WORKDIR /code
COPY . .
RUN poetry install

EXPOSE 8000

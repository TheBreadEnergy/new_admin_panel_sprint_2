FROM python:3.11.5

RUN mkdir /movies_admin

WORKDIR /movies_admin

RUN pip install poetry

RUN poetry config virtualenvs.in-project true

COPY pyproject.toml .

RUN poetry install

COPY . .
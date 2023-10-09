FROM python:3.11.5

RUN mkdir /movies_admin

WORKDIR /movies_admin

COPY pyproject.toml .

RUN pip install poetry && \
    poetry config virtualenvs.in-project true && \
    poetry install

COPY . .

RUN poetry run python manage.py collectstatic

EXPOSE 8000
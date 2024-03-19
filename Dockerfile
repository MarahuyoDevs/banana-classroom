FROM python:3.12-slim

# install poetry
RUN pip install poetry

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY pyproject.toml poetry.lock ./

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

COPY . /app

EXPOSE 5000

CMD [ "poetry","run","granian", "--interface", "asgi", "banana_classroom.frontend.app:frontend_app", "--port", "5000", "--host", "0.0.0.0"]
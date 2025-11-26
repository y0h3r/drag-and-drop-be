FROM python:3.11

WORKDIR /app

RUN pip install --upgrade pip \
    && pip install poetry

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-root --only main

COPY . .

RUN chmod +x /app/start.sh

CMD ["bash", "/app/start.sh"]

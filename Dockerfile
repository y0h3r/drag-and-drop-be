FROM python:3.11

WORKDIR /app

RUN pip install --upgrade pip \
    && pip install poetry

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-root --only main

COPY . .

CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

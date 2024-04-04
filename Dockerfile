FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml ./
COPY lunaflux/ ./lunaflux/
RUN pip install --no-cache-dir -e .
COPY tests/ ./tests/
CMD ["python", "-m", "pytest", "tests/", "-v"]
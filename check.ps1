uv run ruff format .
uv run ruff check . --fix
uv run mypy .
uv run pytest --cov=src --cov-report=term-missing
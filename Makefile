


default: all
all: install run

install:
	setup 3.10 uv

run: test
	.venv/bin/python src/main.py

test: lint
	.venv/bin/python -m pytest

lint:
	.venv/bin/python -m mypy ./src/main.py

clean:
	trash {./venv/,./.venv/}

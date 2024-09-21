


default: all
all: install run

install:
	setup 3.10 uv

run:
	.venv/bin/python src/main.py

clean:
	rm -rf ./.venv
	rm -rf ./venv/

.PHONY: setup test lint clean

setup:
	pip install -e .

test:
	python -m pytest tests/ -v

lint:
	sql-sop check examples/

clean:
	rm -rf dist/ build/ *.egg-info __pycache__

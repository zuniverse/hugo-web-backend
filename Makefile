# Prevent file associations
.PHONY: run-dev test

# What runs if make has no args
# .DEFAULT_GOAL := test

run-dev:
	. venv/bin/activate
	export FLASK_APP=app.main
	export FLASK_ENV=development
	flask run

test:
	python -m tests.test

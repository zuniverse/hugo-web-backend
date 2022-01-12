# Prevent file associations
.PHONY: run-dev test

# What runs if make has no args
# .DEFAULT_GOAL := test

run-dev:
	python3 -m venv venv
	. venv/bin/activate
# python3 -m pip install Flask
	python3 -m pip install -r requirements.txt
	export FLASK_APP=app.main
	export FLASK_ENV=development
	flask run

test:
	python -m tests.test

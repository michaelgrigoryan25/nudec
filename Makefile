.PHONY: run clean

run: setup
	pipenv run flask run

setup:
	pipenv install

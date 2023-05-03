# Local

install-requirements-local:
	pip install -r requirements/local.txt

run-flask-local:
	flask --app main.py run --debug -h 0.0.0.0 -p 5000

shell-local:
	flask --app main.py shell

lint-local:
	pre-commit run -va

lint-update-local:
	pre-commit autoupdate

.PHONY: up down logs test replay classify report risk risk-block flow scenario clean

PYTHON=.venv/bin/python
PYTEST=.venv/bin/pytest

up:
	docker compose up --build -d

down:
	docker compose down

logs:
	docker compose logs -f

test:
	$(PYTEST) -q

scenario:
	docker compose down
	SCENARIO=$(SCENARIO) docker compose up --build -d

replay:
	$(PYTHON) -m incidentos.cli replay --url http://localhost:8000/checkout --traffic traffic/checkout_sample.jsonl

classify:
	$(PYTHON) -m incidentos.cli classify

report:
	$(PYTHON) -m incidentos.cli report

risk:
	$(PYTHON) -m incidentos.cli risk

risk-block:
	$(PYTHON) -m incidentos.cli risk --fail-on HIGH

flow:
	$(PYTHON) -m incidentos.cli flow --url http://localhost:8000/checkout --traffic traffic/checkout_sample.jsonl

clean:
	rm -rf reports/generated .pytest_cache

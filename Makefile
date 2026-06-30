.PHONY: up down logs test replay classify report risk risk-block flow scenario clean

PYTHON=.venv/bin/python
PYTEST=.venv/bin/pytest
CHECKOUT_URL=http://localhost:8000/checkout
TRAFFIC_FILE=traffic/checkout_sample.jsonl

up:
	docker compose up --build -d

down:
	docker compose down

logs:
	docker compose logs -f

test:
	$(PYTEST)

scenario:
	docker compose down
	SCENARIO=$(SCENARIO) docker compose up --build -d

replay:
	$(PYTHON) -m incidentos.cli replay --url "$(CHECKOUT_URL)" --traffic "$(TRAFFIC_FILE)"

classify:
	$(PYTHON) -m incidentos.cli classify

report:
	$(PYTHON) -m incidentos.cli report

risk:
	$(PYTHON) -m incidentos.cli risk

risk-block:
	$(PYTHON) -m incidentos.cli risk --block

flow: replay classify report risk

clean:
	rm -rf reports/generated/*

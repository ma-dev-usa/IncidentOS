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
	$(PYTHON) -m faultscene.cli replay --url "$(CHECKOUT_URL)" --traffic "$(TRAFFIC_FILE)"

classify:
	$(PYTHON) -m faultscene.cli classify

report:
	$(PYTHON) -m faultscene.cli report

risk:
	$(PYTHON) -m faultscene.cli risk

risk-block:
	$(PYTHON) -m faultscene.cli risk --block

flow: replay classify report risk

clean:
	rm -rf reports/generated/*

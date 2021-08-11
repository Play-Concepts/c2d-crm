isort-src:
	isort ./app

format: isort-src
	black ./app

isort-test:
	isort ./app/tests

format-test: isort-test
	black ./app/tests

stop:
	docker-compose down

start: stop
	docker-compose up --build

daemon: stop
	docker-compose up --build -d

dev: stop
	STAGE=dev docker-compose up --build

test:
	STAGE=dev docker-compose --env-file ./env.test -f docker-compose.yml -f docker-compose-test.yml up --build --remove-orphans --exit-code-from datapassport-backend-test

devtest:
	docker-compose exec datapassport-backend pytest -s -v --setup-show app/tests/db/test_customers_log_repository.py

dbconnect:
	docker-compose exec db psql -h localhost -U postgres elyria

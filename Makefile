lint: black-src isort-src flake-src

isort-src:
	isort ./app

black-src:
	black ./app

flake-src:
	flake8 ./app

lint-test: black-test isort-test flake-test

isort-test:
	isort ./app/tests

black-test:
	black ./app/tests

flake-test:
	flake8 ./app/tests

stop:
	docker-compose down

start: stop
	docker-compose up --build

daemon: stop
	docker-compose up --build -d

dev: stop
	STAGE=dev docker-compose up --build

devtest:
	docker-compose exec datapassport-backend pytest -s -v --setup-show app/tests

dbconnect:
	docker-compose exec db psql -h localhost -U postgres elyria

test:
	STAGE=dev docker-compose -f docker-compose-test.yml up --build --remove-orphans --exit-code-from datapassport-backend-test
	$(MAKE) cleantest

cleantest:
	docker rm datapassport-backend_db-test_1
	docker rm datapassport-backend-test
	docker network rm datapassport-backend-testnet

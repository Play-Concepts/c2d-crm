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
	docker-compose exec datapassport-backend pytest -v app/tests

db-connect:
	docker-compose exec db psql -h localhost -U postgres elyria

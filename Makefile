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
	docker-compose up --build -d

test: start
	docker-compose exec datapassport-backend pytest app/tests

dev:
	docker-compose up --build

dev-test:
	docker-compose exec datapassport-backend pytest app/tests

db-connect:
	docker-compose exec db psql -h localhost -U postgres elyria

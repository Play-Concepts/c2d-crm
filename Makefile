isort-src:
	isort ./app

format: isort-src
	black ./app

isort-tests:
	isort ./app/tests

format-tests: isort-test
	black ./app/tests

stop:
	docker-compose down

start: stop
	docker-compose up --build -d

test: start
	docker-compose exec datapassport-backend pytest app/tests

dev:
	docker-compose up --build

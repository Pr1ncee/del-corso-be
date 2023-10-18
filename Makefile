.EXPORT_ALL_VARIABLES:
COMPOSE_FILE ?= ./build/docker-compose/docker-compose.yml
DEL_CORSO_SERVICE ?= del_corso

DOTENV_BASE_FILE ?= .env
-include $(DOTENV_BASE_FILE)


.PHONY: docker-build-all
docker-build-all: docker-build-del-corso

.PHONY: docker-up
docker-up:
	docker compose -f $(COMPOSE_FILE) up -d
	docker compose ps

.PHONY: docker-down
docker-down:
	docker compose down

.PHONY: docker-logs
docker-logs:
	docker compose logs --follow

.PHONY: docker-connect
docker-connect:
	docker compose exec -it $(DEL_CORSO_SERVICE) /bin/bash

.PHONY: makemigrations
makemigrations:
	docker compose exec $(DEL_CORSO_SERVICE) python ./del_corso/manage.py makemigrations

.PHONY: migrate
migrate:
	docker compose exec $(DEL_CORSO_SERVICE) python ./del_corso/manage.py migrate

.PHONY: migrate-zero
migrate-down:
	docker compose exec $(DEL_CORSO_SERVICE) python manage.py migrate zero

.PHONY: init-admin
init-admin:
	docker compose exec $(DEL_CORSO_SERVICE) python ./del_corso/manage.py initadmin

.PHONY: docker-build-del-corso
docker-build-del-corso:
	docker build \
		--tag=del-corso \
		--file=build/docker/del-corso/Dockerfile-del-corso \

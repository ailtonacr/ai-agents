.SILENT:

.DEFAULT_GOAL=help

COLOR_RESET = \033[0m
COLOR_GREEN = \033[32m
COLOR_YELLOW = \033[33m

PROJECT_NAME = `basename $(PWD)`
DOCKER_COMPOSE_FILE = docker-compose.yml

SHELL := /bin/bash

## Shows the available commands.
help:
	printf "${COLOR_YELLOW}\n${PROJECT_NAME}\n\n${COLOR_RESET}"
	awk '/^[a-zA-Z\-\_0-9\.%]+:/ { \
			helpMessage = match(lastLine, /^## (.*)/); \
			if (helpMessage) { \
					helpCommand = substr($$1, 0, index($$1, ":")); \
					helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
					printf "${COLOR_GREEN}$$ make %s${COLOR_RESET} %s\n", helpCommand, helpMessage; \
			} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)
	printf "\n"

## Installs the project dependencies.
setup:
	pip install -r requirements.txt

## Formats the code using Black.
lint:
	black src/ --line-length 118

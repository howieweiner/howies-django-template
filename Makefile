.PHONY: help migrate migrations serve test coverage flake8 lint black mypy tailwind ansible bitwarden buildtailwind deploy dbbackup manage celery
.DEFAULT_GOAL: help

default: help

help: ## Output available commands
	@echo "Available commands:"
	@echo
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

manage: ## Runs Django management command e.g. make manage command="send_test_email"
	DJANGO_READ_DOT_ENV_FILE=1 ./manage.py $(command)

createsuperuser: ## Run database migrations
	DJANGO_READ_DOT_ENV_FILE=1 ./manage.py createsuperuser

migrate: ## Run database migrations
	DJANGO_READ_DOT_ENV_FILE=1 ./manage.py migrate

migrations: ## Make database migrations
	DJANGO_READ_DOT_ENV_FILE=1 ./manage.py makemigrations $(app)

serve: ## Run a local server
	DJANGO_READ_DOT_ENV_FILE=1 ./manage.py runserver 0.0.0.0:8000

tailwind: ## Run tailwind watcher
	DJANGO_READ_DOT_ENV_FILE=1 ./manage.py tailwind start

buildtailwind: ## Run tailwind build
	DJANGO_READ_DOT_ENV_FILE=1 ./manage.py tailwind build

shell: ## Run a Django shell
	DJANGO_READ_DOT_ENV_FILE=1 ./manage.py shell_plus

test: ## Run tests
	DJANGO_READ_DOT_ENV_FILE=1 pytest

testlf: ## Run last-failed tests
	DJANGO_READ_DOT_ENV_FILE=1 pytest --lf

flake8: ## Run flake8
	flake8

lint: ## Run pylint
	DJANGO_READ_DOT_ENV_FILE=1 pylint {{ project_name }}

black: ## Run black
	black .

mypy: ## Run mypy
	DJANGO_READ_DOT_ENV_FILE=1 mypy {{ project_name }}

bitwarden: # Unlock Bitwarden vault
	bash ./scripts/unlock-bitwarden.sh

ansible: ## Run Ansible dev playbook
	ansible-playbook -i infra/environments/$(env) --vault-password-file infra/vault-pass.sh infra/$(playbook).yml

deploy: ## Deploy via Ansible
	ansible-playbook -i infra/environments/$(env) --vault-password-file infra/vault-pass.sh infra/deploy.yml

quickdeploy: ## Quick Deploy via Ansible
	ansible-playbook -i infra/environments/$(env) --vault-password-file infra/vault-pass.sh infra/quickdeploy.yml

dbbackup: ## Backup database
	ansible-playbook -i infra/environments/$(env) --vault-password-file infra/vault-pass.sh infra/dbbackup.yml

celery: ## Run celery
	DJANGO_READ_DOT_ENV_FILE=1 celery -A config worker -l INFO

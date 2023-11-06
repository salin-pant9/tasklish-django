VENV_DIR := "$(HOME)/.pyvenvs"
PYTHON = python3
PROJECT_NAME := $(or $(PROJECT_NAME),$(error PROJECT_NAME is not set. Set it using export PROJECT_NAME=<your_project_name>))

# Django specific
APP ?= ""

# Create a virtual environment
venv:
	@mkdir -p $(VENV_DIR)
	@$(PYTHON) -m venv $(VENV_DIR)/$(PROJECT_NAME)
	@echo "Virtual environment created: $(VENV_DIR)/$(PROJECT_NAME)"
	@echo "Activate with: source $(VENV_DIR)/$(PROJECT_NAME)/bin/activate"
	@echo "Try: \n\n alias activate='source $(VENV_DIR)/$(PROJECT_NAME)/bin/activate'\n"
	@echo "And activate with: activate"

cleanvenv:
	@echo "Removing virtual environment: $(VENV_DIR)/$(PROJECT_NAME)"
	@rm -rf "$(VENV_DIR)/$(PROJECT_NAME)"
	@echo "Done"

resetgit:
	@echo "Removing git directory..."
	@rm -rf .git
	@echo "Re-initializing git directory..."
	@git init
	@echo "Done"

django:
	@python -m pip install --upgrade pip
	@python -m pip install django
	@django-admin startproject "$(PROJECT_NAME)" .

# Install dependencies
install:
	@$(PYTHON) -m pip install --upgrade pip
	@$(PYTHON) -m pip install -r dev.requirements.txt

# Run the Django development server
run:
	@$(PYTHON) manage.py runserver

# create APP
app:
	@$(PYTHON) manage.py startapp $(NAME)

# Makemigrations
migrations:
	@$(PYTHON) manage.py makemigrations $(APP)

# Migrate
migrate:
	@$(PYTHON) manage.py migrate $(APP)

superuser:
	@$(PYTHON) manage.py createsuperuser

.PHONY: venv django install run app makemigrations migrate

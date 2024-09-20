ifneq ("$(wildcard .env)","")
	include .env
	export
endif

.PHONY: install
install: ## Install Python requirements.
	python -m pip install --upgrade pip setuptools wheel poetry
	poetry lock
	poetry install --no-root
	poetry run pre-commit install

.PHONY: runuc
run: ## Rodar melhor agente de Unica Camada
	poetry run python src/app/testagentUC.py

.PHONY: runtrainuc
runtrain: ## Rodar treino de Unica Camada
	poetry run python src/app/mainUC.py

.PHONY: runmc
run: ## Rodar melhor agente de Multi Camadas
	poetry run python src/app/testagentMC.py

.PHONY: runtrainmc
runtrain: ## Rodar treino de Multi Camadas
	poetry run python src/app/mainMC.py


.DEFAULT_GOAL := help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sed 's/Makefile://g' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

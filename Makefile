.PHONY: shell
shell:
	poetry shell

.PHONY: format
format:
	poetry run -- ruff check --fix && ruff format 

.PHONY: lint
lint:
	poetry run -- ruff check && mypy sloth test 
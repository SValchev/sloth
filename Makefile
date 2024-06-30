.PHONY: shell
shell:
	poetry shell

.PHONY: format
format:
	poetry run -- ruff check --fix && ruff format 
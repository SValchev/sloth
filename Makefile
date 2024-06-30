.PHONY: shell
shell:
	poetry shell

.PHONY: format
format:
	poetry run -- black . && isort .
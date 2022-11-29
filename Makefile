# инструкция по работе с файлом "Makefile" – https://bytes.usc.edu/cs104/wiki/makefile/

# обновление сборки Docker-контейнера
build:
	docker compose build

# генерация документации
docs-html:
	docker compose run --workdir /docs references-bot-app /bin/bash -c "make html"

# запуск форматирования кода
format:
	docker compose run --workdir / references-bot-app /bin/bash -c "black src docs/source/*.py; isort --profile black src docs/source/*.py"

# запуск статического анализа кода (выявление ошибок типов и форматирования кода)
lint:
	docker compose run --workdir / references-bot-app /bin/bash -c "mypy src/chatbot.py"

# запуск автоматических тестов
test:
	docker compose run references-bot-app pytest --cov=/src --cov-report html:htmlcov --cov-report term --cov-config=/src/tests/.coveragerc -vv

# запуск всех функций поддержки качества кода
all: format lint test

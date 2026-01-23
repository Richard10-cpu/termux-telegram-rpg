.PHONY: test test-cov test-cov-html clean-cov install help

help: ## Показать эту справку
	@echo "Доступные команды:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Установить зависимости из requirements.txt
	pip install -r requirements.txt

test: ## Запустить все тесты
	pytest

test-cov: ## Запустить тесты с coverage отчётом
	pytest

test-cov-html: test-cov ## Запустить тесты и открыть HTML отчёт
	@echo "Открываю HTML отчёт в браузере..."
	@open htmlcov/index.html 2>/dev/null || xdg-open htmlcov/index.html 2>/dev/null || echo "Откройте файл htmlcov/index.html в браузере"

clean-cov: ## Удалить отчёты coverage
	rm -rf htmlcov/
	rm -f .coverage
	rm -f coverage.json
	@echo "Отчёты coverage удалены"

APP=app.py

export FLASK_APP=$(APP)
export FLASK_ENV=development

.PHONY: all install migrate run

all: install migrate run

install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

migrate:
	@echo "Running migrations..."
	flask db init || true
	flask db migrate
	flask db upgrade

run:
	@echo "Running backend..."
	python $(APP)

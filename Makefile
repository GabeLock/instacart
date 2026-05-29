PYTHON ?= python
PIP ?= pip

.PHONY: setup download-data run-pipeline train-model dashboard test lint clean

setup:
	$(PYTHON) -m venv .venv
	.venv/Scripts/$(PIP) install --upgrade pip
	.venv/Scripts/$(PIP) install -r requirements.txt

download-data:
	$(PYTHON) -m src.ingestion.download_kaggle

run-pipeline:
	$(PYTHON) -m src.orchestration.pipeline

train-model:
	$(PYTHON) -m src.models.train

dashboard:
	streamlit run src/dashboard/app.py

test:
	pytest

lint:
	ruff check .

clean:
	$(PYTHON) -c "import shutil; [shutil.rmtree(p, ignore_errors=True) for p in ['.pytest_cache', '.ruff_cache', '__pycache__']]"


check:
	flake8 .
	mypy .
	python -m pytest --cov=flake8_annotations_complexity --cov-report=xml

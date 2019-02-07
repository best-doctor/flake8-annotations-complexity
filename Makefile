check:
	flake8 .
	mypy .
	pytest --cov=flake8_annotations_complexity --cov-report=xml

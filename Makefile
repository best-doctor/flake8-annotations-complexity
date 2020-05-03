check:
	flake8 .
	mypy .
	python -m pytest --cov=flake8_annotations_complexity --cov-report=xml
	mdl README.md
	safety check -r requirements_dev.txt

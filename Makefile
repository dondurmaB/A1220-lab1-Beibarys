run:
	python -m src.Lab1.main receipts --print

expenses:
	python -m src.Lab1.main receipts --print --expenses $(ARGS)
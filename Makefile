.PHONY: demo test

demo:
	python3 scripts/change_watch.py run customers/example.customer.json

test:
	python3 -m py_compile scripts/change_watch.py monitor.py
	python3 scripts/change_watch.py validate customers/example.customer.json
	python3 scripts/change_watch.py run customers/example.customer.json

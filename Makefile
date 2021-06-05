.PHONY: clean virtualenv test docker dist dist-upload

clean:
	find . -name '*.py[co]' -delete

virtualenv:
	virtualenv --prompt '(ama)' env
	env/bin/pip3 install -r requirements.txt
	@echo
	@echo "VirtualENV Setup Complete. Now run: source env/bin/activate"
	@echo

virtualenv_dev:
	virtualenv --prompt '(ama)' env
	env/bin/pip3 install -r requirements-dev.txt
	@echo
	@echo "VirtualENV Setup Complete. Now run: source env/bin/activate"
	@echo

require:
	python3 -m pip install -r requirements.txt

requiredev:
	python3 -m pip install -r requirements-dev.txt

pkgdev:
	python3 -m pip install . --verbose --use-feature=in-tree-build

dist: clean
	rm -rf dist/*
	python setup.py sdist
	python setup.py bdist_wheel

dist-upload:
	twine upload dist/*

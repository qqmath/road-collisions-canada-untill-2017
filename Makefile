PYTHON=python3

# TODO: might be nice to have a non threading setting
TEST_CONTEXT=export TEST_ENV=True &&

ENV_DIR=.env_$(PYTHON)
IN_ENV=. $(ENV_DIR)/bin/activate &&

env: $(ENV_DIR)

setup:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install virtualenv
	$(PYTHON) -m virtualenv -p $(PYTHON) $(ENV_DIR)
	$(IN_ENV) $(PYTHON) -m pip install --upgrade -r requirements.txt
	$(IN_ENV) $(PYTHON) -m pip install --editable .

test_requirements:
	$(IN_ENV) $(PYTHON) -m pip install --upgrade -r test_requirements.txt

upload_pip: test build_dist
	twine upload --repository road_collisions_canada dist/*

build_dist: setup
	rm -fr dist/
	$(IN_ENV) python setup.py sdist bdist_wheel

build: setup

quick_build:
	$(IN_ENV) $(PYTHON) -m pip install --editable .

test: build test_requirements quick_test

quick_test:
	$(IN_ENV) $(PYTHON) -m unittest

load: setup
	$(IN_ENV) load_road_collisions_canada

PLATFORM = $(shell uname)

PROJECT_NAME=barsky_scrapper
PROJECT_TAG?=barsky_scrapper
GITHUB_PROJECT=ramonlimaramos/barsky-scrapper

VIRTUALENV_ARGS=-p python3.8

PYTHON_MODULES=barsky_scrapper

DOCS_RST?= #${shell find docs -type f -iname '*.rst'}


WGET = wget -q

ifeq "" "$(shell which wget)"
WGET = curl -O -s -L
endif

OK=\033[32m[OK]\033[39m
FAIL=\033[31m[FAIL]\033[39m
CHECK=@if [ $$? -eq 0 ]; then echo "${OK}"; else echo "${FAIL}" ; fi

SQLITE_DATABASE_URI=sqlite:////tmp/barsky-scrapper.db
POSTGRES_DATABASE_URI=postgresql://root:root@localhost:15432/barsky-scrapper-integration

default: help

include extras/makefiles/python.mk

clean: python_clean
	@rm -rf docs/_build

purge: python_purge
	@rm -rf docs/plantuml.jar
	@rm -rf docs/node_modules
	@rm -rf docs/package-lock.json

build: python_build ${CHECKPOINT_DIR}/.python_develop

help: build
	${VIRTUALENV} python ${PYTHON_MODULES}/cli.py -h

local_suspicious: build
	${VIRTUALENV} python ${PYTHON_MODULES}/cli.py --model buick

suspicious:
	docker-compose up --build --exit-code-from barsky-scrapper-cli barsky-scrapper-cli

run: build
	${VIRTUALENV} FLASK_ENV=development FLASK_APP=barsky_scrapper.main flask run

api:
	docker-compose up -d postgres memcached barsky-scrapper-rabbit redis
	docker-compose up --build --exit-code-from barsky-scrapper-flask barsky-scrapper-flask barsky-scrapper-celery barsky-scrapper-celery

test:
	docker-compose -f ./docker-compose.test.yml up --build --exit-code-from barsky-scrapper-test barsky-scrapper-test

local_api: build
	${VIRTUALENV} python -m gunicorn -w 1 -b 0.0.0.0:5000 barsky_scrapper.main:app --log-level=-debug --reload

local_worker: build
	${VIRTUALENV} MODE=WORKER watchmedo auto-restart -d barsky_scrapper -p '*.py' --recursive -- celery -A barsky_scrapper.services.background.main worker -l INFO --no-execv

local_test: build ${REQUIREMENTS_TEST}
	${VIRTUALENV} py.test ${PYTHON_MODULES} --ignore ${PYTHON_MODULES}/tests/integration

pdb: build ${REQUIREMENTS_TEST}
	${VIRTUALENV} CI=1 py.test ${PYTHON_MODULES} -x --ff --pdb --ignore ${PYTHON_MODULES}/tests/integration

coverage: build ${REQUIREMENTS_TEST}
	${VIRTUALENV} CI=1 py.test ${PYTHON_MODULES} --cov=${PYTHON_MODULES} ${PYTHON_MODULES}/tests/ --cov-config .coveragerc --cov-report term-missing --cov-report html:cov_html --cov-report xml:cov.xml --cov-report annotate:cov_annotate

codestyle: ${REQUIREMENTS_TEST}
	${VIRTUALENV} pycodestyle --statistics -qq ${PYTHON_MODULES} | sort -rn || echo ''

report:
	coverage run --source=${PYTHON_MODULES} setup.py test

tox: ${REQUIREMENTS_TEST}
	${VIRTUALENV} python3 -m tox

docs/plantuml-jar-lgpl-1.2019.5.zip:
	cd docs && ${WGET} https://ufpr.dl.sourceforge.net/project/plantuml/1.2019.5/plantuml-jar-lgpl-1.2019.5.zip

docs/plantuml.jar: docs/plantuml-jar-lgpl-1.2019.5.zip
	cd docs && unzip -o plantuml-jar-lgpl-1.2019.5.zip plantuml.jar
	touch $@

docs: ${REQUIREMENTS_TEST} docs/plantuml.jar
	@${VIRTUALENV} $(MAKE) -C docs html

docs/_build/latex/barsky-scrapper.tex: ${REQUIREMENTS_TEST} ${PYTHON_SOURCES} ${DOCS_RST} docs/plantuml.jar
	rm -rf docs/_build/latex
	${VIRTUALENV} $(MAKE) -C docs latex

pdf: docs/_build/latex/barsky-scrapper.tex
	$(MAKE) -C docs/_build/latex

docs_ci: docs/plantuml.jar
	${MAKE} -C docs html

dist: python_egg python_wheel

.PHONY: clean purge dist docs create_db

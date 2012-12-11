# Make File do projeto Atividade Pratica 1
#
# author: Gustavo Pantuza
# since: 10.12.2012

# cria o virtualenv do projeto
env:
	virtualenv .

requirements: REQUIREMENTS
	./bin/pip install -r REQUIREMENTS

run: src/dvcoder/manage.py
	./bin/python src/dvcoder/manage.py runserver 

static: src/dvcoder/manage.py
	./bin/python src/dvcoder/manage.py collectstatic

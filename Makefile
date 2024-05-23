VENV = $(HOME)/.virtualenvs/django-bengalbazaario/bin

lint:
	$(VENV)/isort .;
	$(VENV)/black .;
	$(VENV)/flake8;

server:
	sudo systemctl start postgresql.service
	$(VENV)/python manage.py runserver

update-database:
	$(VENV)/python manage.py makemigrations
	$(VENV)/python manage.py migrate

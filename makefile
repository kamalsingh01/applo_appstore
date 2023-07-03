setup:
	python3 -m venv venv
	source venv/bin/activate
	pip3 install -r requirements.txt --ignore-installed

makemigrations:
	./venv/bin/python manage.py makemigrations

migrate:
	./venv/bin/python manage.py migrate

run:
	./venv/bin/python manage.py runserver
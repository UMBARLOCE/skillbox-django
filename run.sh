#!/bin/bash
# скрипт для старта проекта
# суперпользователь: admin -> admin
# копируем run.sh на рабочий стол и в терминале вводим команду:
# cd ~/Desktop/ && source run.sh

# клонируем проект
cd ~/Desktop/
git clone git@gitlab.skillbox.ru:aleksei_sedykh/Python_django_diploma_dpo.git
cd Python_django_diploma_dpo/

# создаём и активируем виртуальное окружение
python3 -m venv .venv
source .venv/bin/activate

# устанавливаем пакеты
pip install -r requirements.txt

# устанавливаем фронты
cd diploma-frontend/
python setup.py sdist
pip install ./dist/diploma-frontend-0.6.tar.gz

# миграции БД
cd ../megano/
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata all_fixtures.json

# запускаем проект
python manage.py runserver

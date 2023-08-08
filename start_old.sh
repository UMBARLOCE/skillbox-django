#!/bin/bash
# скрипт для первичной настройки
# cd ~/Desktop/ && source start.sh

# клонируем проект
cd ~/Desktop/
git clone git@gitlab.skillbox.ru:aleksei_sedykh/Python_django_diploma_dpo.git

# удаляем старые варианты архива
cd Python_django_diploma_dpo/
rm -R megano/
rm -R diploma-frontend/
cd ~/Desktop/

# # на рабочем столе должна быть папка archive/ с файлами

# обновляем из архива куратора /megano/
cp -R archive/megano/ Python_django_diploma_dpo/megano/

# обновляем из архива куратора /diploma-frontend/
cp -R archive/diploma-frontend/ Python_django_diploma_dpo/diploma-frontend/

# # копируем из архива .gitignore
# cp ./archive/.gitignore ./Python_django_diploma_dpo/.gitignore

# # копируем из архива README.md
# cp ./archive/README.md ./Python_django_diploma_dpo/README.md

# переходим в ветку reload
cd Python_django_diploma_dpo/
git checkout -b reload

# создаём и активируем виртуальное окружение
python3 -m venv .venv
source .venv/bin/activate

# устанавливаем пакеты и морозим зависимости
pip install --upgrade pip
pip install django
pip install Pillow
pip install djangorestframework
pip install django-filter
pip freeze > requirements.txt

# устанавливаем фронты
cd diploma-frontend/
python setup.py sdist
pip install ./dist/diploma-frontend-0.6.tar.gz

# миграции БД
# Уже создан суперпользователь: admin -> 12345
cd ../megano/
python manage.py makemigrations
python manage.py migrate

# запускаем проект
python manage.py runserver

# обновить README.md и start.sh вручную

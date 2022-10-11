# Foodgram

## Workflow
![example workflow](https://github.com/solomen88/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

## Описание 

Проект **Foodgram** создан для людей, увлеченных едой и ее приготовлением. Здесь единомышленники делятся своими фирменными рецептами любимых блюд. Проект позволяет публиковать **рецепты** пользователей, на понравившихся Вам авторов рецептов можно **подписаться**. Рецепты могут быть отсортированы по **тэгам**: завтрак, обед, ужин, супы, дессерты или напитки. Если Вам понравился рецепт, добавьте его в **Избранное**, тогда он точно не потеряется. А в планировании Ваших покупок Вам поможет **Список покупок**, в который Вы можете добавить рецепты, которые планируете приготовить в ближайшее время, а сайт **сформирует Вам в формате PDF список** того, что нужно купить в магазине, и посчитает за Вас количество продуктов.

## Технологический стек

[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=56C0C0&color=008080)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=56C0C0&color=008080)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat&logo=Django%20REST%20Framework&logoColor=56C0C0&color=008080)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat&logo=PostgreSQL&logoColor=56C0C0&color=008080)](https://www.postgresql.org/)
[![JWT](https://img.shields.io/badge/-JWT-464646?style=flat&color=008080)](https://jwt.io/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat&logo=NGINX&logoColor=56C0C0&color=008080)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat&logo=gunicorn&logoColor=56C0C0&color=008080)](https://gunicorn.org/)
[![Docker](https://img.shields.io/badge/-Docker-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker-compose](https://img.shields.io/badge/-Docker%20compose-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker Hub](https://img.shields.io/badge/-Docker%20Hub-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/products/docker-hub)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat&logo=GitHub%20actions&logoColor=56C0C0&color=008080)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat&logo=Yandex.Cloud&logoColor=56C0C0&color=008080)](https://cloud.yandex.ru/)

## Запуск приложения
1. Если у вас уже установлены docker и docker-compose, этот шаг можно пропустить, иначе можно воспользоваться официальной [инструкцией](https://docs.docker.com/engine/install/).
2. Собрать контейнер и запустить
```
docker-compose up -d --build
```
3. Выполнить миграцию базы данных
```
docker-compose exec backend python manage.py migrate --noinput
```
4. Собрать статические файлы
```
docker-compose exec backend python manage.py collectstatic --no-input
```
5. Остановить контейнер
```
docker-compose down
```
## Создание суперпользователя
```
docker-compose run backend python manage.py createsuperuser
```
## Заполнение базы начальными данными
```
sudo docker-compose run backend python manage.py loaddata dump.json
```
## Документация
http://solomen88.ddns.net/api/docs/

## Адрес проекта
http://solomen88.ddns.net/recipes/

## Админка
login: q@q.qq
pass: q

## Автор
Станислав Кучеренко

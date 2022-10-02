# Foodgram

## Workflow
![example workflow](https://github.com/solomen88/foodgram-project-react/actions/workflows/main.yml/badge.svg)

## Описание 

Проект **Foodgram** создан для людей, увлеченных едой и ее приготовлением. Здесь единомышленники делятся своими фирменными рецептами любимых блюд. Проект позволяет публиковать **рецепты** пользователей, на понравившихся Вам авторов рецептов можно **подписаться**. Рецепты могут быть отсортированы по **тэгам**: завтрак, обед, ужин, супы, дессерты или напитки. Если Вам понравился рецепт, добавьте его в **Избранное**, тогда он точно не потеряется. А в планировании Ваших покупок Вам поможет **Список покупок**, в который Вы можете добавить рецепты, которые планируете приготовить в ближайшее время, а сайт **сформирует Вам в формате PDF список** того, что нужно купить в магазине, и посчитает за Вас количество продуктов.

## Технологии

-   Python 3.8.5
-   Django 2.2.19
-   Nginx
-   Gunicorn
-   PostgreSQL

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
Документация будет доступна после запуска проекта по адресу `api/docs/`.

## Адрес проекта
http://solomen88.ddns.net/recipes/

## Администратор
login: q
pass: q

## Автор
Станислав Кучеренко

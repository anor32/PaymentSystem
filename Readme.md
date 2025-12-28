##  проект в рамках тестового задания

## Структура проекта
Проект представляет собой реализацию платежной системы джанго
в проекте используется интеграция со стороним сервисом stripe api
в проекте используется stripe session для коректной работы необходимо получить апи ключ stripe
реализованы модели Order OrderItem Item  для создания заказов отображения их на сайте 

Cтек проекта Python javascript django postgresql Docker

в проекте используется javascript для редиректа на платежную форму stripe

### из тестового задания я реализовал следующие бонусные пункты 
- запуск используя Docker
- Использование environment variables
- Запуск приложения на удаленном сервере, доступном для тестирования, с кредами от админки
- Модель Order, в которой можно объединить несколько Item и сделать платёж в Stripe на содержимое Order c общей стоимостью всех Items
- Модели Discount, Tax,
- поле Item.currency, создать 2 Stripe Keypair на две валюты 


## Требования и подготовка

 Для работы с проектом рекомендуется 
 использовать виртуальное окружение Python (`venv`).

 На вашей системе должны быть установлены:

 - Python 3.12 и выше 
 - pip
 - PostgreSQL 17+
 - docker(опционально)



1**API-ключ stripe**:
   - Можно получить на [Stripe.docs](https://docs.stripe.com/)



### инструкция по установке
1 клонировать репозиторий
```bash
    git clone https://github.com/anor32/TgBotAnalyst
    cd TgBotAnalyst
```

2 создать виртуально окружение либо использовать уже готовое
```bash
    python -m venv venv
    venv/Scripts/activate 
```

3 установить зависимости
```
pip install --upgrade pip
pip install -r requirements.txt

```
4. создать env файл заполнить его согласно файлу env_sample

### запуск проекта
cоздание базы данных
```bash 
   python -m backend.commands.manage_db -op create 
```
проведение миграций 
5. Создайте базу данных и выполните миграции:

```bash
    python manage.py ccdb
    python manage.py makemigrations
   python manage.py migrate
```

6. Создайте пользователей с помощью кастомной команды:

   ```bash
   python manage.py ccsu
   ```
   
7. Загрузите начальные данные из фикстур:

   ```bash
   python -Xutf8 manage.py loaddata backup/products.json
   python -Xutf8 manage.py loaddata backup/users.json

## Запуск проекта с помощью Docker

### Требования#
 - Docker
 - Docker Compose

 ### Инструкция

### для запуска контейнера пропишите следующую команду
убедитесь, что пользователь и данные для входа в базу данных актуальны.
поумолчанию создается локальный контейнер, подключеный  к
стандартному порту postgres
поднять собрать образ и поднять контейнер
```bash
    docker-compose up  --build
   
```
остановить контейнер
```bash
docker-compose down 
```
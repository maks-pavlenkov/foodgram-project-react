# Foodgram

Сервис рецептов: создай свой, ищи чужие, сохраняй себе или формируй список покупок!


## Техстэк

**Client:** React

**Server:** Python 3.9, Django 2.2.16, DRF 3.12.4

### Как подключиться к серверу:
- Ввести команду
```
edm_people@158.160.29.232
```
- Пароль
```
Qq123456
```
- Логин и пароль админа
```
admin qwe123
```

### Как запустить проект:

- Клонировать репозиторий:

```
git clone https://github.com/maks-pavlenkov/foodgram-project-react.git
```
- Перейти в директорию и создать виртуальное окружение командой python3 -m venv venv
- Активировать виртуальное окружение командой - source venv/bin/activate
- Установить все зависимости командой - pip install -r requirements.txt
- Запустить проект командой python manage.py runserver


## Регистрация и аутентификация:
- [POST: users](http://127.0.0.1:8000/api/users/)
- [POST: token](http://127.0.0.1:8000/api/auth/token/)

## API Endpoints:
- [GET: recipes](http://127.0.0.1:8000/api/recipes/)
- [GET: tags](http://127.0.0.1:8000/api/tags/)
- [GET: ingredients](http://127.0.0.1:8000/api/ingredients/)
- [GET: users](http://127.0.0.1:8000/api/users/)


#### Примеры запроса:

```http
  GET http://127.0.0.1:8000/api/tags/
```

#### Ответ:

```javascript
[
    {
        "id": 0,
        "name": "Завтрак",
        "color": "#E26C2D",
        "slug": "breakfast"
    }
]
```


```http
  GET http://127.0.0.1:8000/api/ingredients/
```

#### Ответ:

```javascript
[
  {
    "id": 0,
    "name": "Капуста",
    "measurement_unit": "кг"
  }
]
```


```http
  GET http://127.0.0.1:8000/api/recipes/
```

#### Ответ:

```javascript
{
  "count": 123,
  "next": "http://foodgram.example.org/api/recipes/?page=4",
  "previous": "http://foodgram.example.org/api/recipes/?page=2",
  "results": [
    {
      "id": 0,
      "tags": [
        {
          "id": 0,
          "name": "Завтрак",
          "color": "#E26C2D",
          "slug": "breakfast"
        }
      ],
      "author": {
        "email": "user@example.com",
        "id": 0,
        "username": "string",
        "first_name": "Вася",
        "last_name": "Пупкин",
        "is_subscribed": false
      },
      "ingredients": [
        {
          "id": 0,
          "name": "Картофель отварной",
          "measurement_unit": "г",
          "amount": 1
        }
      ],
      "is_favorited": true,
      "is_in_shopping_cart": true,
      "name": "string",
      "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
      "text": "string",
      "cooking_time": 1
    }
  ]
}
```

## Authors

Павленков Максим
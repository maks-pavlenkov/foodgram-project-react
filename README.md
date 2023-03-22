# Foodgram

Сервис рецептов: создай свой, ищи чужие, сохраняй себе или формируй список покупок!


## Техстэк

**Client:** React

**Server:** Python 3.9, Django 2.2.16, DRF 3.12.4

### Как запустить проект:

Клонировать репозиторий:

```
git clone https://github.com/maks-pavlenkov/foodgram-project-react.git
```

## Регистрация и аутентификация:
- [POST: users](http://127.0.0.1:8000/api/users/)
- [POST: token](http://127.0.0.1:8000/api/auth/token/)

## API Endpoints:
- [GET: recipes](http://127.0.0.1:8000/api/recipes/)
- [GET: tags](http://127.0.0.1:8000/api/tags/)
- [GET: ingredients](http://127.0.0.1:8000/api/ingredients/)
- [GET: users](http://127.0.0.1:8000/api/users/)


#### Пример запроса:

```http
  GET http://jinglemybells.sytes.net/api/tags/
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

## Authors

Павленков Максим
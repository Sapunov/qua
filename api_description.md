# Описание API

## Методы


### Поиск

- GET **/search** - поиск по введенному тексу
    - query - текст запроса
    - limit - размер выдачи
    - offset - сдвиг в выдаче
    - category -  название категории относительно которой нужно искать


### Вопросы

- GET **/questions** - список всех вопросов
    - limit
    - offset
    - category
- POST **/questions** - создание нового вопроса
- GET **/questions/&lt;int:question_id&gt;** - выбор конкретного запроса по `question_id`
- PUT **/questions/&lt;int:question_id&gt;** - обновление данных в вопросе `question_id`
- DELETE **/questions/&lt;int:question_id&gt;** - архивирование вопроса `question_id`


### Категории

- GET **/categories** - список всех категорий
    - limit
    - offset
- POST **/categories** - добавление новой категории
- GET **/categories/&lt;int:category_id&gt;** - информация о категории `category_id`
- PUT **/categories/&lt;int:category_id&gt;** - обновление данных категории `category_id`
- DELETE **/category/&lt;int:category_id&gt;** - архивирование категории `category_id`



## Описание ответа API

Если при выполнении запроса не было никаких ошибок, то API вернет ответ в следующем формате:

```
{
    "ok": 1,
    "data": {...}
}
```

Если при выполнении запроса возникла ошибка, ответ вернется в следующем виде:

```
{
    "ok": 0,
    "error": {
        "error_code": 100,
        "error_msg": "...",
        "error_description": "..."
    }
}
```
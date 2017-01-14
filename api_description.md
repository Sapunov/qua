# Описание API


## Общее

API разрешает посылать к себе запросы со следующими методами:

- **GET**
- **POST**
- **PUT**
- **DELETE**
- **OPTIONS**

При успешном выполнении запроса всегда будет HTTP статус ответа - **200**

При ошибке, имеют место быть следующие коды HTTP:

- **HTTP_400_BAD_REQUEST** (если ошибка не поддается классификации приведенной ниже)
- **HTTP_401_UNAUTHORIZED** (если не указан JWT)
- **HTTP_403_FORBIDDEN** (если действие не разрешено)
- **HTTP_404_NOT_FOUND** (если сущность не найдена)
- **HTTP_405_METHOD_NOT_ALLOWED** (если данный endpoint не поддерживает запрос данного типа)


## Описание ответа API

Если при выполнении запроса не было никаких ошибок, то API вернет ответ в следующем формате:

```
{
    "ok": 1,
    "response": {...} (или null)
}
```

Если при выполнении запроса возникла ошибка, ответ вернется в следующем виде:

```
{
    "ok": 0,
    "error": {
        "error_code": 100,
        "error_msg": "...",
    }
}
```


## Авторизация

Для авторизации используется JWT (Json Web Token).
В данный момент реализовано простое получение токена со сроком протухания 1 неделя, то есть через неделю нужно будет
заново спросить у пользователя логин и пароль.
**Фронтенд должен поддерживать обработку таких ситуаций**

Для получения JWT:

`POST` **/api/auth** {'username': 'example', 'password': 'secret_password'}

При успешном ответе API отдаст следующий ответ:

```
{
    "ok": 1,
    "response": {
        "token": "<NEW_JWT_TOKEN>"
    }
}
```

При неудаче будет выведено сообщение об ошибке и ответ HTTP будет **400**:

```
{
    "error": {
        "error_code": 400,
        "error_msg": "Unable to login with provided credentials."
    },
    "ok": 0
}
```

По истечение срока действия JWT будет выведено следующее сообщение:

```
{
    "error": {
        "error_code": 401,
        "error_msg": "Signature has expired."
    },
    "ok": 0
}
```



## Методы


### Поиск

- GET **/search** - поиск по введенному тексу
    - query - текст запроса
    - limit - размер выдачи
    - offset - сдвиг в выдаче
    - category -  название категории относительно которой нужно искать

Формат данных:

`GET` **/api/search?query=друг**

```
{
    "ok": 1,
    "response": {
        "category_assumptions": null,
        "hits": [
            {
                "categories": [
                    {
                        "id": 1,
                        "name": "Привет"
                    }
                ],
                "id": 1,
                "image": null,
                "keywords": [],
                "score": 1.0,
                "snippet": "Привет тебе друг",
                "title": "Привет тебе друг",
                "url_params": {
                    "qid": 1,
                    "shid": 47,
                    "token": "91727aa95d47fcdc9966"
                }
            }
        ],
        "query": "друг",
        "total": 1
    }
}
```


### Вопросы

- GET **/questions** - список всех вопросов
    - limit
    - offset
    - category
- POST **/questions** - создание нового вопроса
- GET **/questions/&lt;int:question_id&gt;** - выбор конкретного запроса по `question_id`
- PUT **/questions/&lt;int:question_id&gt;** - обновление данных в вопросе `question_id`
- DELETE **/questions/&lt;int:question_id&gt;** - архивирование вопроса `question_id`

Формат выходных данных при запросе одного вопроса

`GET` **/api/questions/1**

```
{
    "ok": 1,
    "response": {
        "answer": {
            "created_at": "2017-01-08T00:14:45.323298Z",
            "created_by": {
                "first_name": "",
                "id": 1,
                "last_name": "",
                "username": "nsapunov"
            },
            "html": "<p>првиет</p>",
            "id": 1,
            "raw": "првиет",
            "snippet": "фывафыва",
            "updated_at": "2017-01-08T00:14:45.323372Z",
            "updated_by": {
                "first_name": "",
                "id": 1,
                "last_name": "",
                "username": "nsapunov"
            },
            "version": 1
        },
        "categories": [
            {
                "id": 1,
                "name": "Привет"
            }
        ],
        "created_at": "2017-01-07T22:47:48.373734Z",
        "created_by": {
            "first_name": "",
            "id": 1,
            "last_name": "",
            "username": "nsapunov"
        },
        "id": 1,
        "keywords": [],
        "title": "Привет тебе друг",
        "updated_at": "2017-01-11T22:17:42.385153Z",
        "updated_by": {
            "first_name": "",
            "id": 1,
            "last_name": "",
            "username": "nsapunov"
        }
    }
}

```

Формат выходных данных при запросе списка вопросов.

Вместо поля `answer` выдается `answer_exists` с булевым значением есть ответ на вопрос или нет.

`GET` **/api/questions**

```
{
    "ok": 1,
    "response":     [
        {
            "answer_exists": true,
            "categories": [
                {
                    "id": 4,
                    "name": "привет"
                },
                {
                    "id": 12,
                    "name": "жопа-2"
                }
            ],
            "created_at": "2017-01-14T09:51:52.428555Z",
            "created_by": {
                "first_name": "",
                "id": 1,
                "last_name": "",
                "username": "nsapunov"
            },
            "id": 49,
            "keywords": [
                "привет",
                "nikita",
                "слон"
            ],
            "title": "привет",
            "updated_at": "2017-01-14T09:51:52.451319Z",
            "updated_by": {
                "first_name": "",
                "id": 1,
                "last_name": "",
                "username": "nsapunov"
            }
        },
        {
            "answer_exists": false,
            "categories": [],
            "created_at": "2017-01-14T10:36:54.865758Z",
            "created_by": {
                "first_name": "",
                "id": 1,
                "last_name": "",
                "username": "nsapunov"
            },
            "id": 50,
            "keywords": [
                "слон"
            ],
            "title": "Джигурда",
            "updated_at": "2017-01-14T10:36:54.884780Z",
            "updated_by": {
                "first_name": "",
                "id": 1,
                "last_name": "",
                "username": "nsapunov"
            }
        }
    ]
}
```


Формат данных для добавления/изменения вопроса

```
{
    "title": "some title",
    "keywords": ["one", "two", "three"],
    "categories": [{"id": 1}, {"id": 3}],
    "answers": {"raw": "some markdown"}
}
```

При добавлении обязательным элементом является `title`, при изменении все поля необязательные и будет изменено только то поле, которое указано.


### Категории

- GET **/categories** - список всех категорий
    - limit
    - offset
- POST **/categories** - добавление новой категории
- GET **/categories/&lt;int:category_id&gt;** - информация о категории `category_id`
- PUT **/categories/&lt;int:category_id&gt;** - обновление данных категории `category_id`
- DELETE **/category/&lt;int:category_id&gt;** - архивирование категории `category_id`

Формат данных:

`GET` **/api/categories/1**

```
{
    "ok": 1,
    "response": {
        "created_at": "2017-01-07T22:46:26.603318Z",
        "created_by": {
            "first_name": "",
            "id": 1,
            "last_name": "",
            "username": "nsapunov"
        },
        "id": 1,
        "name": "Привет",
        "updated_at": "2017-01-07T22:46:26.603410Z",
        "updated_by": {
            "first_name": "",
            "id": 1,
            "last_name": "",
            "username": "nsapunov"
        }
    }
}
```

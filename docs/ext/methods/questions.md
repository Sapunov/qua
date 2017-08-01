### Вопросы

- GET **/questions** - список всех вопросов
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
            "answer_exists": true,
            "updated_at": "2017-01-08T00:14:45.323372Z",
            "updated_by": {
                "first_name": "",
                "id": 1,
                "last_name": "",
                "username": "nsapunov"
            },
            "version": 1
        },
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
    - limit - сколько результатов должно быть получено
    - offset - сдвиг относительно начала набора результатов

```
{
    "ok":1,
    "response":{
        "items":[
            {
                "answer_exists":true,
                "created_at":"2017-01-14T09:51:52.428555Z",
                "created_by":{
                    "first_name":"",
                    "id":1,
                    "last_name":"",
                    "username":"nsapunov"
                },
                "id":49,
                "keywords":[
                    "привет",
                    "nikita",
                    "слон"
                ],
                "title":"привет",
                "updated_at":"2017-01-14T09:51:52.451319Z",
                "updated_by":{
                    "first_name":"",
                    "id":1,
                    "last_name":"",
                    "username":"nsapunov"
                }
            },
            {
                "answer_exists":false,
                "created_at":"2017-01-14T10:36:54.865758Z",
                "created_by":{
                    "first_name":"",
                    "id":1,
                    "last_name":"",
                    "username":"nsapunov"
                },
                "id":50,
                "keywords":[
                    "слон"
                ],
                "title":"Джигурда",
                "updated_at":"2017-01-14T10:36:54.884780Z",
                "updated_by":{
                    "first_name":"",
                    "id":1,
                    "last_name":"",
                    "username":"nsapunov"
                }
            },
            ...
        ],
        "total":22,
        "pagination":{
            "next":"/api/questions?offset=20&limit=10",
            "prev":"/api/questions?offset=10&limit=10"
        }
    }
}
```


Формат данных для добавления/изменения вопроса

```
{
    "title": "some title",
    "keywords": ["one", "two", "three"],
    "answers": {"raw": "some markdown"}
}
```

При добавлении обязательным элементом является `title`, при изменении все поля необязательные и будет изменено только то поле, которое указано.

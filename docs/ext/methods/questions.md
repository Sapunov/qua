## /questions


- GET **/questions** - список всех вопросов
- POST **/questions** - создание нового вопроса
- GET **/questions/&lt;int:question_id&gt;** - выбор конкретного запроса по `question_id`
- PUT **/questions/&lt;int:question_id&gt;** - обновление данных в вопросе `question_id`
- DELETE **/questions/&lt;int:question_id&gt;** - архивирование вопроса `question_id`


### `GET` /questions

Без параметров метод возвращает 10 вопросов в порядке убывания рейтинга.

**Параметры**:
- **limit** - количество вопросов для вывода (по умолчанию: 10)
- **offset** - сдвиг относительно первого вопроса в порядке убывания рейтинга (по умолчанию: 0)
- **keyword** - при заданном ключевом слове будут выведены только те вопросы, в которых есть данное ключевое слово


**Формат ответа**:

```json
{
	"items": [],
	"total": <int>,
	"pagination": {}
}
```

Каждый *item* имеет следующие поля:

```json
{
	"answer_exists": <bool>,
	"created_at": <string>"2017-01-14T09:51:52.428555Z",
	"created_by": {
		"first_name": <string>,
		"id": <int>,
		"last_name": <string>,
		"username": <string>
	},
	"id": <int>,
	"keywords": [<string>, <string>, ...],
	"title": <string>,
	"updated_at": <string>"2017-01-14T09:51:52.428555Z",
	"updated_by": {
		"first_name": <string>,
		"id": <int>,
		"last_name": <string>,
		"username": <string>
	}
}

```

Объект *pagination* содержит 2 ссылки:

```json
{
	"next":"/api/questions?offset=20&limit=10",
    "prev":"/api/questions?offset=10&limit=10"
}
```


### `POST` /questions

У данного метода нет параметров.


**Формат данных для добавления вопроса:**:

```json
{
    "title": <string>,
    "keywords": [<string>, <string>, ...],
    "answer": {"raw": <string>}
}
```

Обязательное поле - **title**. Все остальные поля необязательные.
Если вопрос создается без ответа, то будет создан неотвеченный вопрос с
соответствующей логикой. Если вопрос создаётся сразу с ответом, то это будет полноценная запись с вопросом и ответом, которая будет присутствовать в поисковой выдаче. Неотвеченные вопросы не участвуют в поиске.

В качестве **raw** может быть передан *markdown*, который будет отрендерен.


**Формат ответа**:

В качестве ответа на данный запрос вернется полноценный вопрос со всеми полями. Список всех полей можно увидеть в части [/questions/&lt;int:question_id&gt;](#`get`-/questions/&lt;int:question_id&gt;)
Статус ответа в случае успешного сохранения вопроса будет *200*.


### `GET` /questions/&lt;int:question_id&gt;

У данного метода нет параметров


**Формат ответа(вопрос со всеми полями)**:

```json
{
	"answer": {
		"created_at": <string>"2017-01-14T09:51:52.428555Z",
		"created_by": {
			"first_name": <string>,
			"id": <int>,
			"last_name": <string>,
			"username": <string>
		},
		"html": <string>,
		"id": <int>,
		"raw": <string>,
		"answer_exists": <bool>,
		"updated_at": <string>"2017-01-14T09:51:52.428555Z",
		"updated_by": {
			"first_name": <string>,
			"id": <int>,
			"last_name": <string>,
			"username": <string>
		},
		"version": <int>
	},
	"created_at": <string>"2017-01-14T09:51:52.428555Z",
	"created_by": {
		"first_name": <string>,
		"id": <int>,
		"last_name": <string>,
		"username": <string>
	},
	"id": <int>,
	"keywords": [<string>, <string>, ...],,
	"title": <string>,
	"updated_at": <string>"2017-01-14T09:51:52.428555Z",
	"updated_by": {
		"first_name": <string>,
		"id": <int>,
		"last_name": <string>,
		"username": <string>
	},
}
```


### `PUT` /questions/&lt;int:question_id&gt;

У данного метода нет параметров


**Формат данных для изменения вопроса:**

```json
{
    "title": <string>,
    "keywords": [<string>, <string>, ...],
    "answer": {"raw": <string>}
}
```

Ни одно из полей не является обязательным. Будет изменено только то поле,
которое было передано. Изменения будут применены только в том случае,
если новая версия данных отличается от старой. Например, если передается
тот же заголовок, что и был ранее, то никаких изменений вопроса не
произойдет.


**Формат ответа:**

В качестве ответа на данный запрос вернется полноценный вопрос со всеми полями. Список всех полей можно увидеть в части [/questions/&lt;int:question_id&gt;](#`get`-/questions/&lt;int:question_id&gt;)
Статус ответа в случае успешного сохранения вопроса будет *200*.


### `DELETE` /questions/&lt;int:question_id&gt;

У данного метода нет параметров


**Формат ответа:**

При успешном выполнении запроса вернется *200* ответ сервера.
Данный метод ничего не возвращает, то есть, если посмотреть на ответ сервера, то будет вот так:

```json
{
	"ok": 1,
	"response": null
}
```

**Внимание! ** В данном примере приведен именно ответ сервера, а не
формат ответа метода. Поля *ok* и *response* имеются у любого ответа
сервиса *ext*. Больше информации об ответе микросервиса - [response](../response.md).

# Прокт развёрнут

https://file-storage.nks-tech.ru/

OpenAPI https://file-storage.nks-tech.ru/api/openapi

## Запуск для разработки

```sh
docker compose watch
```

## Проектное задание пятого спринта

Вам необходимо спроектировать и разработать файловое хранилище, которое позволяет хранить различные типы файлов — документы, фотографии, другие данные.

## Описание задания

Реализовать **http-сервис**, который обрабатывает поступающие запросы. Сервер стартует по адресу `http://127.0.0.1:8080` (дефолтное значение, может быть изменено).

<details>
<summary> Список необходимых эндпойнтов. </summary>

1. Статус активности связанных сервисов.

    <details>
    <summary> Описание изменений. </summary>

    ```
    GET /ping
    ```
    Получить информацию о времени доступа ко всем связанным сервисам, например, к БД, кэшам, примонтированным дискам и т.д.

    **Response**
    ```json
    {
        "db": 1.27,
        "cache": 1.89,
        ...
        "service-N": 0.56
    }
    ```
   </details>


2. Регистрация пользователя.

    <details>
    <summary> Описание изменений. </summary>

    ```
    POST /register
    ```
    Регистрация нового пользователя. Запрос принимает на вход логин и пароль для создания новой учетной записи.

    </details>


3. Авторизация пользователя.

    <details>
    <summary> Описание изменений. </summary>

    ```
    POST /auth
    ```
    Запрос принимает на вход логин и пароль учетной записи и возвращает авторизационный токен. Далее все запросы проверяют наличие токена в заголовках - `Authorization: Bearer <token>`

    </details>


4. Информация о загруженных файлах.

    <details>
    <summary> Описание изменений. </summary>

    ```
    GET /files/
    ```
    Вернуть информацию о ранее загруженных файлах. Доступно только авторизованному пользователю.

    **Response**
    ```json
    {
        "account_id": "AH4f99T0taONIb-OurWxbNQ6ywGRopQngc",
        "files": [
              {
                "id": "a19ad56c-d8c6-4376-b9bb-ea82f7f5a853",
                "name": "notes.txt",
                "created_ad": "2020-09-11T17:22:05Z",
                "path": "/homework/test-fodler/notes.txt",
                "size": 8512,
                "is_downloadable": true
              },
            ...
              {
                "id": "113c7ab9-2300-41c7-9519-91ecbc527de1",
                "name": "tree-picture.png",
                "created_ad": "2019-06-19T13:05:21Z",
                "path": "/homework/work-folder/environment/tree-picture.png",
                "size": 1945,
                "is_downloadable": true
              }
        ]
    }
    ```
    </details>


5. Загрузить файл в хранилище.

    <details>
    <summary> Описание изменений. </summary>

    ```
    POST /files/upload
    ```
    Метод загрузки файла в хранилище. Доступно только авторизованному пользователю.
    Для загрузки заполняется полный путь до файла, в который будет загружен/переписан загружаемый файл. Если нужные директории не существуют, то они должны быть созданы автоматически.
    Так же есть возможность указать только путь до директории. В этом случае имя создаваемого файла будет создано в соответствии с передаваемым именем файла.

    **Request**
    ```
    {
        "path": <full-path-to-file>||<path-to-folder>,
    }
    ```

    **Response**
    ```json
    {
        "id": "a19ad56c-d8c6-4376-b9bb-ea82f7f5a853",
        "name": "notes.txt",
        "created_ad": "2020-09-11T17:22:05Z",
        "path": "/homework/test-fodler/notes.txt",
        "size": 8512,
        "is_downloadable": true
    }
    ```
    </details>


6. Скачать загруженный файл.

    <details>
    <summary> Описание изменений. </summary>

    ```
    GET /files/download
    ```
    Скачивание ранее загруженного файла. Доступно только авторизованному пользователю.

    **Path parameters**
    ```
    /?path=<path-to-file>||<file-meta-id>
    ```
    Возможность скачивания есть как по переданному пути до файла, так и по идентификатору.
    </details>

</details>




## Требования к решению

1. В качестве СУБД используйте PostgreSQL (не ниже 10 версии).
2. Опишите [docker-compose](docker-compose.yml) для разработки и локального тестирования сервисов.
3. Используйте концепции ООП.
4. Предусмотрите обработку исключительных ситуаций.
5. Приведите стиль кода в соответствие pep8, flake8, mypy.
6. Логируйте результаты действий.
7. Покройте написанный код тестами.

# Hotel Service

Простой сервис для управления номерами отелей и бронированиями.  
Реализован на Django с использованием слоистой архитектуры (Models → Repositories → Services → Views).  

Сервис позволяет добавлять, удалять и получать номера отелей, так же реализован CRUD с бронями.

## Эндпоинты для тестирования
У нас есть следующие эндпоинты:

Номера отеля:

POST /rooms/create — создать номер.
DELETE /rooms/delete — удалить номер.
GET /rooms/list — получить список номеров.


Бронирования:

POST /bookings/create — создать бронирование.
DELETE /bookings/delete — удалить бронирование.
GET /bookings/list?room_id=<id> — получить список бронирований для номера.



Ниже я опишу, как настроить запросы в Postman для каждого эндпоинта и проверить их работу.

Тестирование эндпоинтов в Postman
1) POST /rooms/create — Создание номера

- Цель: Создать новый номер отеля.
- Шаги:

1) В Postman создайте новый запрос:

    - Метод: POST
    - URL: http://localhost:8000/rooms/create


2) Перейдите на вкладку Body, выберите raw, и установите тип данных JSON.
3) Введите JSON для создания номера (на основе RoomCreateSerializer)

```bash
{
  "number": "101",
  "price_per_night": 100.00,
  "description": "Standard room with one bed",
  "is_available": true
}
```

4) Отправьте на сервер

Ожидаемый результат:

- Код ответа: 201 Created
- Тело ответа (JSON):
```json
{
  "room_id": 1
}
```

Ошибка (если данные некорректны, например, отсутствует number):
```json
{
  "error": {
    "number": ["This field is required."]
  }
}
```



2. GET /rooms/list — Получение списка номеров

- Цель: Получить список всех номеров с возможностью сортировки.
- Шаги:

1) Создайте новый запрос:

    - Метод: GET
    - URL: http://localhost:8000/rooms/list


2) (Опционально) Добавьте параметры сортировки в URL, например:

- `http://localhost:8000/rooms/list?sort_by=price&order=desc` — сортировка по цене по убыванию.
- `http://localhost:8000/rooms/list?sort_by=created_at&order=asc` — сортировка по дате создания по возрастанию.


3) Нажмите Send.


Ожидаемый результат:

- Код ответа: 200 OK
- Тело ответа (JSON, пример для двух номеров):
```json
[
  {
    "id": 1,
    "number": "101",
    "price_per_night": "100.00",
    "is_available": true,
    "description": "Standard room with one bed",
    "created_at": "2025-10-13T12:00:00Z",
    "updated_at": "2025-10-13T12:00:00Z"
  },
  {
    "id": 2,
    "number": "102",
    "price_per_night": "150.00",
    "is_available": true,
    "description": "Deluxe room",
    "created_at": "2025-10-13T12:05:00Z",
    "updated_at": "2025-10-13T12:05:00Z"
  }
]
```



3) DELETE /rooms/delete — Удаление номера

- Цель: Удалить номер и связанные с ним бронирования.
- Шаги:

1. Создайте новый запрос:

   - Метод: DELETE
   - URL: http://localhost:8000/rooms/delete


2. Перейдите на вкладку Body, выберите raw, и установите тип данных JSON.
3. Введите JSON с идентификатором номера
```json
{
  "room_id": 1
}
```
4. Нажмите Send.
Ожидаемый результат:

- Код ответа: 204 No Content (успешное удаление, без тела ответа).
- Ошибка (если номер не найден):
```json
{
  "error": "Номер не найден"
}
```


4. POST /bookings/create — Создание бронирования

- Цель: Создать новое бронирование для номера.
- Шаги:

1) Создайте новый запрос:

   - Метод: POST
   - URL: http://localhost:8000/bookings/create


2) Перейдите на вкладку Body, выберите raw, и установите тип данных JSON.
3) Введите JSON для создания бронирования (на основе BookingCreateSerializer):
```json
{
  "room_id": 1,
  "date_start": "2025-11-01",
  "date_end": "2025-11-03"
}
```
4. Нажмите Send.
Ожидаемый результат:

Код ответа: 201 Created
Тело ответа (JSON):
```json
{
  "booking_id": 1
}
```
- Ошибки (примеры):

   - Если date_end не позже date_start:
```json
{
  "error": "date_end must be after date_start"
}
```
5. GET /bookings/list — Получение списка бронирований

- Цель: Получить список бронирований для указанного номера.
- Шаги:

1) Создайте новый запрос:

   - Метод: GET
   - URL: http://localhost:8000/bookings/list?room_id=1


2) Убедитесь, что параметр room_id указан в URL.
3) Нажмите Send.


- Ожидаемый результат:

   - Код ответа: 200 OK
   - Тело ответа (JSON, пример для двух бронирований)

```json
[
  {
    "id": 1,
    "room_id": 1,
    "check_in": "2025-11-01",
    "check_out": "2025-11-03",
    "created_at": "2025-10-13T12:10:00Z"
  },
  {
    "id": 2,
    "room_id": 1,
    "check_in": "2025-11-05",
    "check_out": "2025-11-07",
    "created_at": "2025-10-13T12:15:00Z"
  }
]
```

6. DELETE /bookings/delete — Удаление бронирования

- Цель: Удалить бронирование по его ID.
- Шаги:

1) Создайте новый запрос:

   - Метод: DELETE
   - URL: http://localhost:8000/bookings/delete


2) Перейдите на вкладку Body, выберите raw, и установите тип данных JSON.
3) Введите JSON с идентификатором бронирования:
```json
{
  "booking_id": 1
}
```
4) Отправьте запрос.
Ожидаемый результат:

Код ответа: 204 No Content (успешное удаление, без тела ответа).  
Ошибка (если бронирование не найдено):
```json
{
  "error": "Бронь не найдена"
}
```
Код ответа: 404 Not Found.  
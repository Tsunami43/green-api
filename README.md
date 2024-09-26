# GreenAPI Python Library

GreenAPI Python Library — это асинхронная библиотека для взаимодействия с API GreenAPI, который предоставляет автоматизацию для WhatsApp сообщений. Она упрощает отправку сообщений, получение уведомлений и управление состоянием API-инстанса.

## Возможности

- **Отправка сообщений в WhatsApp**: Удобный способ отправлять сообщения в чаты.
- **Получение уведомлений**: Получайте уведомления о событиях, таких как новые сообщения.
- **Управление инстансом**: Проверка состояния, выход из аккаунта и настройка параметров инстанса.
- **Асинхронные запросы**: Использование библиотеки `httpx` для выполнения запросов в асинхронном режиме.

## Установка

### Шаг 1: Клонирование репозитория

Клонируйте проект с GitHub в ваш проект:

```bash
pip install https://github.com/Tsunami43/green_api.git
```

## Использование
Для начала работы с библиотекой создайте объект GreenApi, указав ID инстанса и токен, которые можно получить на панели управления GreenAPI.
```python
from greenapi import GreenApi

# Создание инстанса GreenApi
api = GreenApi(idInstance="your_instance_id", apiTokenInstance="your_api_token")

# Пример: Отправка сообщения
await api.send_message(chat_id="1234567890@c.us", text="Привет от GreenApi!")
```

### Основные методы
* get_state_instance(): Проверить состояние вашего инстанса GreenAPI.
* authorization_code(phone: int): Запросить код авторизации для номера телефона.
* get_wa_status(): Получить текущий статус WhatsApp инстанса.
* wa_log_out(): Выйти из аккаунта WhatsApp инстанса.
* receive_notification(): Получить уведомления и события, такие как новые сообщения.
* delete_notification(receiptId: int): Удалить уведомление по идентификатору.
* send_message(chat_id: str, text: str, reply_message_id: Optional[str] = None, link_preview: bool = False): Отправить сообщение в чат.


### Пример отправки сообщения
```python
# Отправка сообщения в чат
await api.send_message(chat_id="1234567890@c.us", text="Привет! Как дела?")

```
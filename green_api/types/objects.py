import time
from httpx import Response
from .errors import *

class Message:
    def __init__(self, data: dict):
        if "timestamp" in data:
            t: float = data['timestamp']
            local = time.localtime(t)
            self.timestamp = time.asctime(local)
        else:
            raise KeyNotFound("timestamp", data)
        

        if "idMessage" in data:
            self.message_id: str = data['idMessage']
        else:
            raise KeyNotFound("idMessage", data)
        
        if "senderData" in data:
            senderData: dict = data['senderData']

            if "chatId" in senderData:
                self.chat_id: str = senderData['chatId']
            else:
                raise KeyNotFound("chatId", data, self.message_id)

            if "sender" in senderData:
                self.sender: str = senderData['sender']
            else:
                raise KeyNotFound("sender", data, self.message_id)

            if self.chat_id!=self.sender:
                raise GroupMessage(data)

            if "chatName" in senderData:
                self.chat_name: str = senderData['chatName']
            else:
                self.chat_name = None
            
        else:
            raise KeyNotFound("senderData", data, self.message_id)



        if "messageData" in data:
            messageData: dict = data['messageData']

            if "typeMessage" in messageData:
                match (messageData['typeMessage']):
                    case ('textMessage'):
                        if "textMessage" in messageData['textMessageData']:
                            self.text: str = messageData['textMessageData']['textMessage']
                        else:
                            raise KeyNotFound("textMessage", data, self.message_id)

                    case ('quotedMessage'):
                        if "text" in messageData['extendedTextMessageData']:
                            self.text: str = messageData['extendedTextMessageData']['text']
                        else:
                            raise KeyNotFound("text", data, self.message_id)

                    case (_):
                        raise OtherMessage(data)
            else:
                raise KeyNotFound("typeMessage", data, self.message_id)
            
        else:
            raise KeyNotFound("messageData", data, self.message_id)


class Status:
    is_closed: bool
    message: str

    def __init__(self, is_closed: bool, message: str):
        self.is_closed = is_closed
        self.message = message


class Response:

    def __init__(self, response: Response):
        self.response = response
        if self.response.status_code != 200:
            raise ErrorRequest(response)

    def json(self):
        return self.response.json()

    def on_event(self)-> Message:
        self.receiptId = self.response.json()['receiptId']
        body = self.response.json()['body']
        
        if body['typeWebhook'] == 'incomingMessageReceived':
            return Message(body)    
        else:
            raise ErrorType(body)

    def state(self)-> bool:
        state = self.response.json()['stateInstance']
        if state=="authorized":
            return True
        else:
            return False

    def status(self)-> Status:
        state = self.response.json()['stateInstance']
        if state=="notAuthorized":
            return Status(
                True,
                "Аккаунт не авторизован."
            )
        if state=="authorized":
            return Status(
                False,
                f"Аккаунт авторизован.\n\n👤 +{self.response.json()['phone']}"
            )
        if state=="blocked":
            return Status(
                True,
                "Аккаунт забанен."
            )
        if state=="sleepMode":
            return Status(
                False,
                f"<b>Статус устарел.</b> Аккаунт ушел в спящий режим. Состояние возможно, когда выключен телефон. После включения телефона может потребоваться до 5 минут для перевода состояния аккаунта в значение <b>Авторизован.</b>\n\n👤 +{self.response.json()['phone']}"
            )
        if state=="starting":
            return Status(
                True,
                "Аккаунт в процессе запуска (сервисный режим). Происходит перезагрузка инстанса, сервера или инстанс в режиме обслуживания. Может потребоваться до 5 минут для перевода состояния аккаунта в значение <b>Авторизован.</b>"
            )
        if state=="yellowCard":
            return Status(
                False,
                f"На аккаунте частично или полностью приостановлена отправка сообщений из-за спамерской активности.\n\n👤 +{self.response.json()['phone']}"
            )
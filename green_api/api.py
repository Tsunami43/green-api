import json
import logging
from typing import Optional
from httpx import AsyncClient, ReadTimeout
from .types.objects import *
from .types.errors import *


class GreenApi:
    def __init__(
        self,
        idInstance: str,
        apiTokenInstance: str,
        host: str = "https://api.green-api.com",
    ):
        self.host = host

        self.idInstance = idInstance
        self.apiTokenInstance = apiTokenInstance

        self.session = AsyncClient()

        self.logger = logging.getLogger(__name__)

    def get_url(self, method: str = "") -> str:
        return (
            self.host
            + "/waInstance"
            + self.idInstance
            + method
            + "/"
            + self.apiTokenInstance
        )

    async def get_state_instance(self) -> bool:
        url = self.get_url("/getStateInstance")

        try:
            response = Response(await self.session.get(url))
            return response.state()
        except ErrorRequest as error:
            self.logger.error("ErrorRequest", error.message)
            return False

        except Exception as ex:
            self.logger.error(ex)
            return False

    async def authorization_code(self, phone: int) -> str:
        url = self.get_url("/getAuthorizationCode")

        payload = {"phoneNumber": phone}

        try:
            response = Response(
                await self.session.post(url, data=json.dumps(payload), timeout=30)
            )
        except ReadTimeout:
            response = False
        except ErrorRequest as error:
            response = False
            self.logger.error("ErrorRequest", error.message)
        except Exception as ex:
            response = False
            self.logger.error(ex)
        finally:
            if (response, Response):
                if response.json()["status"]:
                    response = response.json()["code"]
            return response

    async def get_wa_status(self) -> str:
        url = self.get_url("/getWaSettings")

        try:
            response = Response(await self.session.get(url))
        except ReadTimeout:
            response = response = Status(True, "Превышено время ожидания!")
        except ErrorRequest as error:
            response = Status(True, "Ошибка на сервере!")
            self.logger.error("ErrorRequest", error.message)
        except Exception as ex:
            response = Status(True, "Неизвестная ошибка!")
            self.logger.error(ex)
        finally:
            if (response, Response):
                return response.status()
            return response

    async def wa_log_out(self) -> bool:
        url = self.get_url("/logout")

        try:
            response = Response(await self.session.get(url))
        except ReadTimeout:
            response = False
        except ErrorRequest as error:
            response = False
            self.logger.error("ErrorRequest", error.message)
        except Exception as ex:
            response = False
            self.logger.error(ex)
        finally:
            if (response, Response):
                return response.json()["isLogout"]
            return response

    async def receive_notification(self):
        url = self.get_url("/receiveNotification")
        response = None
        message = None

        try:
            response = Response(await self.session.get(url))
            message = response.on_event()

        except KeyNotFound as error:
            self.logger.error(error.message + error.data)

        except GroupMessage as error:
            self.logger.error(error.message + error.data)

        except OtherMessage as error:
            self.logger.error(error.message + error.data)

        except ErrorType as error:
            self.logger.error(error.message + error.data)

        except ErrorRequest as error:
            self.logger.error("ErrorRequest", error.message)

        except ReadTimeout:
            pass

        except Exception as ex:
            self.logger.error(ex)

        finally:
            if isinstance(response, Response):
                await self.delete_notification(response.receiptId)
            return message

    async def delete_notification(self, receiptId: int):
        url = self.get_url("/deleteNotification") + "/" + str(receiptId)

        try:
            response = Response(await self.session.delete(url))

        except ErrorRequest as error:
            self.logger.error("ErrorRequest", error.message)

        except Exception as ex:
            self.logger.error(ex)

    async def send_message(
        self,
        chat_id: str,
        text: str,
        reply_message_id: Optional[str] = None,
        link_preview: bool = False,
    ):

        url = self.get_url("/sendMessage")

        headers = {"Content-Type": "application/json"}

        payload = {"chatId": chat_id, "message": text, "linkPreview": link_preview}
        if reply_message_id != None:
            payload["quotedMessageId"] = reply_message_id

        try:
            response = Response(
                await self.session.post(url, headers=headers, data=json.dumps(payload))
            )

        except ErrorRequest as error:
            self.logger.error("ErrorRequest", error.message)

        except Exception as ex:
            self.logger.error(ex)

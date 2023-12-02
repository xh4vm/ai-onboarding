from gigachat import GigaChat

from src.models.message import MessageData
from src.core.config import GIGACHAT_CONFIG


class GigachatService:

    def chat(self, message: MessageData, **kwargs):
        with GigaChat(
            credentials=GIGACHAT_CONFIG.SECRET,
            verify_ssl_certs=False
        ) as giga:
            response = giga.chat(message.message)
            return response.choices[0].message.content

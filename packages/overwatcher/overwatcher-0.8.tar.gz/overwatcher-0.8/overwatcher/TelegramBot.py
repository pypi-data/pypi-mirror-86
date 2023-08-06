from typing import Union

import telegram


class TelegramBot:
    def __init__(self, token: str, chat_id: Union[int, str]):
        self.bot = telegram.Bot(token=token)
        self.chat_id = chat_id

    def send_file(self, path: str, text: str = '', overflow_error_message: str = None):
        try:
            self.bot.send_document(chat_id=self.chat_id, document=open(path, 'rb'), caption=text)
        except OverflowError:
            if overflow_error_message is not None:
                self.send_message(overflow_error_message)

    def send_message(self, text: str = ''):
        self.bot.send_message(chat_id=self.chat_id, text=text, parse_mode=telegram.ParseMode.MARKDOWN)

import telebot
from loguru import logger
import os
import time
from telebot.types import InputFile
import json
from polybot.caption_parser import CaptionParser
from polybot.error import NoCaptionError
from polybot.response_types import ErrorTypes


class Bot:

    def __init__(self, token, telegram_chat_url):
        # create a new instance of the TeleBot class.
        # all communication with Telegram servers are done using self.telegram_bot_client
        self.telegram_bot_client = telebot.TeleBot(token)

        # remove any existing webhooks configured in Telegram servers
        self.telegram_bot_client.remove_webhook()
        time.sleep(0.5)

        # set the webhook URL
        self.telegram_bot_client.set_webhook(url=f'{telegram_chat_url}/{token}/', timeout=60)

        logger.info(f'Telegram Bot information\n\n{self.telegram_bot_client.get_me()}')

    def send_text(self, chat_id, text):
        self.telegram_bot_client.send_message(chat_id, text)

    def send_text_with_quote(self, chat_id, text, quoted_msg_id, parse_mode = None):
        self.telegram_bot_client.send_message(chat_id, text, reply_to_message_id = quoted_msg_id, parse_mode = parse_mode)

    def is_current_msg_photo(self, msg):
        return 'photo' in msg

    def download_user_photo(self, msg):
        """
        Downloads the photos that sent to the Bot to `photos` directory (should be existed)
        :return:
        """
        if not self.is_current_msg_photo(msg):
            raise RuntimeError(f'Message content of type \'photo\' expected')

        file_info = self.telegram_bot_client.get_file(msg['photo'][-1]['file_id'])
        data = self.telegram_bot_client.download_file(file_info.file_path)
        folder_name = file_info.file_path.split('/')[0]

        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        with open(file_info.file_path, 'wb') as photo:
            photo.write(data)

        return file_info.file_path

    def send_photo(self, chat_id, img_path):
        if not os.path.exists(img_path):
            raise RuntimeError("Image path doesn't exist")

        self.telegram_bot_client.send_photo(
            chat_id,
            InputFile(img_path)
        )

    def handle_message(self, msg):
        """
        Bot Main message handler
        """

        logger.info(f'Incoming message: {msg}')
        self.send_text(msg['chat']['id'], f'Your original message: {msg["text"]}')


class QuoteBot(Bot):
    def handle_message(self, msg):
        logger.info(f'Incoming message: {msg}')

        if msg["text"] != 'Please don\'t quote me':
            self.send_text_with_quote(msg['chat']['id'], msg["text"], quoted_msg_id=msg["message_id"])


class ImageProcessingBot(Bot):

    TIMEOUT = 30

    def __init__(self, token, telegram_chat_url):
        super().__init__(token, telegram_chat_url)
        self.cache = {}
        with open('polybot/reply_templates/Image_processing_bot_replies.json') as replies_file:
            self.replies = json.loads(replies_file.read())

    def handle_message(self, msg):
        logger.info(f'Incoming message: {msg}')
        if msg['from']['id'] in self.cache and msg['message_id'] <= self.cache[msg['from']['id']]:
            return

        self.__clean_cache(msg['date'], ImageProcessingBot.TIMEOUT)

        # Separate logic between text messages and photo messages
        if self.is_current_msg_photo(msg):
            self.__handle_photo_message(msg)
        else:
            self.__handle_text_message(msg)

    def __clean_cache(self, curr_time, timeout):
        """
        Delete all older than 'timeout' messages in the cache

        :param curr_time: Current time: Unix time as integer
        :param timeout: Timeout to delete old messages: positive integer in seconds
        """

        for user_id, msg in self.cache:
            if curr_time - msg["date"] > timeout:
                del self.cache[user_id]

    def __handle_text_message(self, msg):
        text = self.replies['text'][msg['text']] if 'text' in msg\
                                                 and msg['text'] in self.replies['text']\
                                                 else self.replies['text']['unknown']

        self.send_text_with_quote(msg['chat']['id'], text,
                                  quoted_msg_id=msg['message_id'])

    def __handle_photo_message(self, msg):
        if 'caption' in msg:
            commands = CaptionParser.parse(msg['caption'])
            if len(commands) == 0 or commands[0] is NoCaptionError:
                self.send_text_with_quote(msg['chat']['id'],
                                          self.replies['photo'][ErrorTypes.NO_CAPTION],
                                          quoted_msg_id=msg['message_id'])
                return

            doubles = (command.double for command in commands)
            # TODO: handle caption
            print(doubles)
        else:
            user_id = msg['from']['id']

            # verify if the current image is grouped with the previous photo message
            if (user_id in self.cache
                    and 'caption' in self.cache[user_id]
                    and 'media_group_id' in msg
                    and 'media_group_id' in self.cache[user_id]
                    and msg['media_group_id'] == self.cache['media_group_id']):
                # TODO: handle caption
                pass
            else:
                self.send_text_with_quote(msg['chat']['id'],
                                          self.replies['photo'][ErrorTypes.NO_CAPTION],
                                          quoted_msg_id=msg['message_id'])

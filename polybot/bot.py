import re
import string

import telebot
from loguru import logger
import os
import time
from telebot.types import InputFile
import json
from enum import Enum
from polybot.caption_parser import CaptionParser, EffectCommand
from polybot.error import NoCaptionError, CommandError
from polybot.img_proc import Img
from polybot.response_types import DocumentTypes, ErrorTypes, Photo, Text, Help


class Bot:

    class ParseMode(Enum):
        TEXT = None
        MARKDOWN = 'MarkdownV2'

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
        self.telegram_bot_client.send_message(chat_id, text, disable_web_page_preview = True)

    def send_text_with_quote(self, chat_id, text, quoted_msg_id, parse_mode = ParseMode.TEXT.value):
        self.telegram_bot_client.send_message(chat_id, text, reply_to_message_id = quoted_msg_id, parse_mode = parse_mode, disable_web_page_preview = True)

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

    def send_photo(self, chat_id, img_path, caption = None, quoted_msg_id = None, parse_mode = ParseMode.TEXT.value):
        if not os.path.exists(img_path):
            raise RuntimeError("Image path doesn't exist")
        self.telegram_bot_client.send_photo(
            chat_id,
            InputFile(img_path),
            caption,
            parse_mode,
            reply_to_message_id = quoted_msg_id
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

    with open('polybot/reply_templates/Image_processing_bot_replies.json') as replies_file:
        REPLIES = json.loads(replies_file.read())

    def __init__(self, token, telegram_chat_url):
        super().__init__(token, telegram_chat_url)
        self.cache = {}

    def handle_message(self, msg):
        logger.info(f'Incoming message: {msg}')
        if msg['from']['id'] in self.cache and msg['message_id'] <= self.cache[msg['from']['id']]['message_id']:
            return

        self.__clean_cache(msg['date'], ImageProcessingBot.TIMEOUT)

        # Separate logic between text messages and photo messages
        if self.is_current_msg_photo(msg):
            self.__handle_photo_message(msg)
        elif 'document' in msg:
            self.__reply_error(msg, DocumentTypes.Document, 'text')
        else:
            if not self.__reply_help(msg):
                self.__handle_text_message(msg)

    def __parse_response(self, response_type, args = (), category = 'photo', parse_mode = Bot.ParseMode.MARKDOWN.value):
        if args:
            # Stringify args and handle special characters in Telegram's MarkdownV2
            if parse_mode == Bot.ParseMode.MARKDOWN.value:
                for i, arg in enumerate(args):
                    if type(arg) is not str:
                        arg = str(arg)
                    args[i] = re.sub(r'(?<!\\)[_*\[\]()~`>#+\-=|{}.!]', r'\\\g<0>', arg)

            response = f'{self.REPLIES[category][response_type].format(*args)}'
        else:
            response = self.REPLIES[category][response_type]

        return response

    def __reply_text(self, msg, response_type = None, response_args = (), category = 'text', text = None, parse_mode = Bot.ParseMode.MARKDOWN.value):
        if not text:
            text = self.__parse_response(response_type, response_args, category, parse_mode)

        self.send_text_with_quote(
            msg['chat']['id'], text,
            msg['message_id'],
            parse_mode=Bot.ParseMode.MARKDOWN.value)

    def __reply_error(self, msg, error_type = None, error_args = (), text = None):
        if not text:
            text = self.__parse_response(error_type, error_args)
        else:
            text = re.sub(r'(?<!\\)[_*\[\]()~`>#+\-=|{}.!]', r'\\\g<0>', text)

        text += f'\n{self.REPLIES['general'][ErrorTypes.ENDING]}'

        self.send_text_with_quote(
            msg['chat']['id'], text,
            msg['message_id'],
            parse_mode=Bot.ParseMode.MARKDOWN.value)

    def __reply_photo(self, msg, photo_path):
        self.send_photo(
            msg['chat']['id'],
            photo_path,
            self.__parse_response(Photo.SEND),
            msg['message_id'],
            parse_mode = self.ParseMode.MARKDOWN.value
        )

    def __reply_help(self, msg):
        if 'text' not in msg: return False

        request = msg['text'].strip().lower()

        if not request.startswith('help'):
            return False

        if request == 'help':
            self.__reply_text(msg, Help.HELP, category='help')
            return True

        effect_name = msg['text'][len('help '):].replace('-', '_')

        if effect_name not in self.REPLIES['help']:
            self.__reply_text(msg, Help.UNKNOWN, [request[len('help '):]], 'help')
        else:
            self.__reply_text(msg, effect_name, category = 'help')

        return True

    def __clean_cache(self, curr_time, timeout):
        """
        Delete all older than 'timeout' messages in the cache

        :param curr_time: Current time: Unix time as integer
        :param timeout: Timeout to delete old messages: positive integer in seconds
        """

        for user_id, msg in self.cache.items():
            if curr_time - msg["date"] > timeout:
                del self.cache[user_id]

    def __handle_text_message(self, msg):
        if 'text' in msg and msg['text'] in self.REPLIES['text']:
            self.__reply_text(msg, msg['text'])
        else:
            self.__reply_text(msg, Text.UNKNOWN)

    def __handle_photo_message(self, msg):
        if 'caption' in msg:
            commands = CaptionParser.parse(msg['caption'].lower())

            if len(commands) == 0 or type(commands[0]) is NoCaptionError:
                self.__reply_error(msg, ErrorTypes.NO_CAPTION)
                return

            got_command_errors = self.__handle_command_errors(msg, commands)
            if got_command_errors: return

            multies = []
            for command in commands:
                if command.multi:
                    multies.append(command.command_name)

            if self.__handle_multies_errors(msg, commands, multies):
                return

            if self.__handle_args_errors(msg, commands):
                return

            if len(multies) == 1 and 'media_group_id' in msg:
                msg['commands'] = commands
                self.cache[msg['from']['id']] = msg
                return
            else:
                self.__reply_text(msg, Photo.PROCESSING, category='photo')

                result_path, [source_img] = self.__process_image([msg], commands)
                self.__reply_photo(msg, result_path)
                source_img.delete()
                source_img.path = result_path
                source_img.delete()

        else:
            user_id = msg['from']['id']
            # verify that the current image is grouped with the previous photo message
            if (user_id in self.cache
                    and 'caption' in self.cache[user_id]
                    and 'media_group_id' in msg
                    and 'media_group_id' in self.cache[user_id]
                    and msg['media_group_id'] == self.cache[user_id]['media_group_id']):
                cached_msg = self.cache[user_id]

                if 'used' in cached_msg: return

                if 'commands' not in self.cache[user_id] or not self.cache[user_id]['commands']:
                    self.__reply_error(msg, ErrorTypes.NO_CAPTION)
                    return

                self.__reply_text(msg, Photo.PROCESSING, category='photo')

                result_path, source_imgs = self.__process_image([cached_msg, msg], cached_msg['commands'])
                self.__reply_photo(msg, result_path)
                for img in source_imgs:
                    img.delete()
                source_imgs[0].path = result_path
                source_imgs[0].delete()
                self.cache[user_id]['used'] = True
            else:
                self.__reply_error(msg, ErrorTypes.NO_CAPTION)

    def __handle_command_errors(self,msg, commands):
        error_responses = []
        for command in commands:
            if type(command) is CommandError:
                error_responses.append(self.__parse_response(command.error_type, command.error_args))

        if len(error_responses) > 0:
            self.__reply_error(msg, text = '\n'.join(error_responses))
            return True

        return False

    def __handle_multies_errors(self, msg, commands, multies):
        if len(multies) > 0:
            if 'media_group_id' not in msg:
                self.__reply_error(msg, ErrorTypes.NO_2ND_IMAGE, [multies[0]])

                return True
            if len(multies) > 1:
                self.__reply_error(msg, ErrorTypes.TOO_MUCH_MULTI_IMAGE, ['\n'.join(multies)])

                # store the msg as used, so the other grouped images will be ignored
                msg['used'] = True
                self.cache[msg['from']['id']] = msg

                return True

    def __handle_args_errors(self, msg, commands):
        commands_with_errors = []
        for command in commands:
            error_args_list = list(filter(lambda arg: type(arg) is CommandError, command.arg_list))
            if len(error_args_list) > 0:
                commands_with_errors.append(EffectCommand(error_args_list[0].error_args[0],
                                                          error_args_list))

        if len(commands_with_errors) > 0:
            def parse_command_errors(command):
                def parse_arg(arg):
                    text = f'{arg.error_args[-1]}: {self.__parse_response(arg.error_type, arg.error_args)}'
                    # text += str.format(self.REPLIES['photo'][arg.error_type],
                    #             *arg.error_args)
                    return text
                parsed_args = list(map(parse_arg, command.arg_list))

                return self.__parse_response(
                    ErrorTypes.ARG_ERROR,
                    [
                        command.arg_list[0].error_args[0],
                        '\n'.join(parsed_args)
                ])

            parsed_responses = list(map(parse_command_errors, commands_with_errors))
            self.__reply_error(msg, text = '\n\n'.join(parsed_responses))
            return True

        return False

    def __process_image(self, msgs, commands):
        imgs = list(map(lambda msg: Img(self.download_user_photo(msg)), msgs))

        for command_data in commands:
            command = getattr(imgs[0], command_data.command_name)
            if command_data.multi:
                command(imgs[1], *command_data.arg_list)
            else:
                command(*command_data.arg_list)

        return imgs[0].save_img(), imgs
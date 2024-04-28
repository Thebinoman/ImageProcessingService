"""
Telegram Bot
"""

# pylint: disable=E0401
import re
import os
import time
import json
from enum import Enum

import telebot
from loguru import logger
from telebot.types import InputFile
from polybot.caption_parser import CaptionParser, EffectCommand
from polybot.error import NoCaptionError, CommandError
from polybot.img_proc import Img
from polybot.response_types import DocumentTypes, ErrorTypes, Photo, Text, Help
# pylint: enable=E0401


class Bot:
    """
    Base functionality for a Telegram bot.
    Have useful methods to create Telegram bots
    by inheriting from this class.
    """

    class ParseMode(Enum):
        """
        Enum of possible parse modes
        """

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
        """
        Send a simple message

        :param chat_id: Required. The chat to send the message to. Usually msg['chat]['id'].
        :param text: Required. The content of the message to send.
        """
        self.telegram_bot_client.send_message(chat_id, text, disable_web_page_preview = True)

    def send_text_with_quote(self, chat_id, text, quoted_msg_id, parse_mode = ParseMode.TEXT.value):
        """
        Send a text message as a reply

        :param chat_id: Required. The chat to send the message to. Usually msg['chat]['id'].
        :param text: Required. The content of the message to send.
        :param quoted_msg_id: Required. The ID of the message to reply to.
        :param parse_mode: Optional: Can be None for regular text, 'MarkdownV2' or 'HTML'.
        """

        self.telegram_bot_client.send_message(
            chat_id, text,
            reply_to_message_id = quoted_msg_id,
            parse_mode = parse_mode,
            disable_web_page_preview = True
        )

    def is_current_msg_photo(self, msg):
        """
        Check if the given message contains a photo

        :param msg: Required. The message to check.
        :return: True if photo found or False if not.
        """

        return 'photo' in msg

    def download_user_photo(self, msg):
        """
        Downloads the photos that sent to the Bot to `photos` directory (should be existed)

        :return: String of the path to the downloaded image
        """
        if not self.is_current_msg_photo(msg):
            raise RuntimeError('Message content of type \'photo\' expected')

        file_info = self.telegram_bot_client.get_file(msg['photo'][-1]['file_id'])
        data = self.telegram_bot_client.download_file(file_info.file_path)
        folder_name = file_info.file_path.split('/')[0]

        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        with open(file_info.file_path, 'wb') as photo:
            photo.write(data)

        return file_info.file_path

    # pylint: disable=R0913
    def send_photo(
            self, chat_id, img_path,
            caption = None, quoted_msg_id = None,
            parse_mode = ParseMode.TEXT.value):
        """
        Sends an image back to the Telegram user

        :param chat_id: Required. The chat to send the image to. Usually msg['chat]['id'].
        :param img_path: Required. The path to the image file.
        :param caption: Optional: The caption to send with the image. Default is None (no caption).
        :param quoted_msg_id: Optional: To send as reply, insert the message ID to reply to.
               Usually msg['message_id']. Default is None (not as reply, but a regular message).
        :param parse_mode: Optional: Can be None for regular text, 'MarkdownV2' or 'HTML'.
               For more info go to: https://core.telegram.org/bots/api. Default is None
        """
        if not os.path.exists(img_path):
            raise RuntimeError("Image path doesn't exist")
        self.telegram_bot_client.send_photo(
            chat_id,
            InputFile(img_path),
            caption,
            parse_mode,
            reply_to_message_id = quoted_msg_id
        )
    # pylint: enable=R0913

    def handle_message(self, msg):
        """
        Bot Main message handler
        """

        logger.info(f'Incoming message: {msg}')
        self.send_text(msg['chat']['id'], f'Your original message: {msg["text"]}')


class QuoteBot(Bot):
    """
    Quote Bot is simply echoing the user input from the Telegram bot
    as a reply to the original message
    """
    def handle_message(self, msg):
        logger.info(f'Incoming message: {msg}')

        if msg["text"] != 'Please don\'t quote me':
            self.send_text_with_quote(
                msg['chat']['id'], msg["text"],
                quoted_msg_id=msg["message_id"]
            )


class ImageProcessingBot(Bot):
    """
    Image Processing Bot handles the Telegram API
    to process the images and responds according to user input
    """

    # Timeout to clean old messages from cache
    TIMEOUT = 30

    # Set REPLIES to hold all reply messages
    with open(
            'polybot/replies/Image_processing_bot_replies.json',
            encoding="utf-8"
    ) as replies_file:
        REPLIES = json.loads(replies_file.read())

    def __init__(self, token, telegram_chat_url):
        super().__init__(token, telegram_chat_url)
        self.cache = {}

    def handle_message(self, msg):
        """
        Main function to handle all incoming messages
        :param msg: Required. The incoming message.
        """

        # Log incoming message
        logger.info(f'Incoming message: {msg}')

        # Checks if this message is already handled
        if (msg['from']['id'] in self.cache
                and msg['message_id'] <= self.cache[msg['from']['id']]['message_id']):
            return

        # Clean old messages from the cache
        self.__clean_cache(msg['date'], ImageProcessingBot.TIMEOUT)

        # Separate logic between text messages and photo messages
        if self.is_current_msg_photo(msg):
            self.__handle_photo_message(msg)
        # returns error if images are not compressed
        elif 'document' in msg:
            self.__reply_error(msg, DocumentTypes.Document, 'text')
        # Is msg is a text message
        else:
            # Handle help messages
            if not self.__reply_help(msg):
                # If msg not a help message, check and handle if it's other text message
                self.__handle_text_message(msg)

    def __parse_response(
            self, response_type,
            args = (), category = 'photo',
            parse_mode = Bot.ParseMode.MARKDOWN.value):
        """
        Parse a reply according to the replies file, and passed arguments

        :param response_type: Required. The response type = the key from the replies file.
        :param args: Sometimes Required. The arguments that will be injected into the reply.
        :param category: Optional. The category that response_type is from. Default is 'photo'.
        :param parse_mode: Optional. Can be None or 'MarkdownV2'.
               Cannot be 'HTML'. Default is 'MarkdownV2'
        :return: The parsed response as a string
        """

        if args:
            # Stringify args and handle special characters in Telegram's MarkdownV2
            if parse_mode == Bot.ParseMode.MARKDOWN.value:
                for i, arg in enumerate(args):
                    if not isinstance(arg, str):
                        arg = str(arg)
                    args[i] = re.sub(r'(?<!\\)[_*\[\]()~`>#+\-=|{}.!]', r'\\\g<0>', arg)

            # Parse the response
            response = f'{self.REPLIES[category][response_type].format(*args)}'
        else:
            # Parse the response with no args
            response = self.REPLIES[category][response_type]

        return response

    # pylint: disable=R0913
    def __reply_text(self,
                     msg, response_type = None,
                     response_args = (),
                     category = 'text', text = None,
                     parse_mode = Bot.ParseMode.MARKDOWN.value):
        """
        Reply a text message to the user

        :param msg: Required. The original message from the user.
        :param response_type: Required. The response type = the key from the replies file.
        :param response_args: Sometimes Required. The arguments that will be
               injected into the reply.
        :param category: Optional: The category from the replies file. Default is 'text'.
        :param text: Optional. Text as a reply instead of using the reply system.
               If used, response_type, response_args and category will be ignored.
        :param parse_mode:
        """

        # If not using 'text' argument, parse the response with reply system
        if not text:
            text = self.__parse_response(response_type, response_args, category, parse_mode)

        # send the reply
        self.send_text_with_quote(
            msg['chat']['id'], text,
            msg['message_id'],
            parse_mode=Bot.ParseMode.MARKDOWN.value)

    def __reply_error(self, msg, error_type = None, error_args = (), text = None):
        """
        Reply an error back to the user when the sent text has a problem

        :param msg: Required. The original message from the user.
        :param error_type: Required. The error (response) type = the key from the replies file.
        :param error_args: Sometimes Required. The arguments that will be injected into the reply.
        :param text: Optional. Text as a reply instead of using the reply system.
        """

        # If not using 'text' argument, parse the response with reply system
        if not text:
            text = self.__parse_response(error_type, error_args)
        else:
            # If using 'text', parse it to match 'MarkdownV2'
            text = re.sub(r'(?<!\\)[_*\[\]()~`>#+\-=|{}.!]', r'\\\g<0>', text)

        # Add consistent ending to the error reply
        text += f'\n{self.REPLIES['general'][ErrorTypes.ENDING]}'

        # Send the error reply
        self.send_text_with_quote(
            msg['chat']['id'], text,
            msg['message_id'],
            parse_mode=Bot.ParseMode.MARKDOWN.value)
    # pylint: enable=R0913

    def __reply_photo(self, msg, photo_path):
        """
        Reply an image

        :param msg: Required. The original message from the user.
        :param photo_path: Required. The path to the image file.
        """

        # Send the replied image
        self.send_photo(
            msg['chat']['id'],
            photo_path,
            self.__parse_response(Photo.SEND),
            msg['message_id'],
            parse_mode = self.ParseMode.MARKDOWN.value
        )

    def __reply_help(self, msg):
        """
        Check if the given message is a 'help' message,
        handle and reply to the message

        :param msg: Required. The original message from the user.
        """
        # If no text is in the message, this is not a 'help' message
        if 'text' not in msg:
            return False

        # Fetch and treat the text of the message
        request = msg['text'].strip().lower()

        # If the message is not starting with the keyword 'help',
        # it is not a 'help' message.
        if not request.startswith('help'):
            return False

        # Is the message is the main help request (without an effect name)
        if request == 'help':
            # Reply with the main help reply
            self.__reply_text(msg, Help.HELP, category='help')
            return True

        # Fetch the effect name from the request
        effect_name = request[len('help '):].replace('-', '_')

        # If effect_name is not in the replies file,
        # reply with the reply with unknown help request
        if effect_name not in self.REPLIES['help']:
            self.__reply_text(msg, Help.UNKNOWN, [request[len('help '):]], 'help')
        else:
            # Send help reply, related to the effect_name
            self.__reply_text(msg, effect_name, category = 'help')

        return True

    def __clean_cache(self, curr_time, timeout):
        """
        Delete all older than 'timeout' messages in the cache

        :param curr_time: Current time: Unix time as integer
        :param timeout: Timeout to delete old messages: positive integer in seconds
        """

        # Iterate over all cashed messages
        for user_id, msg in self.cache.items():
            # If a message is older than 'timeout'
            if curr_time - msg["date"] > timeout:
                # Delete the message from cache
                del self.cache[user_id]

    def __handle_text_message(self, msg):
        """
        Check if the given message is a 'text' message,
        handle and reply to the message

        :param msg: Required. The original message from the user.
        """

        # If there is text in the message, and there is a corresponding
        # key in the replies system, reply to the message
        if 'text' in msg and msg['text'] in self.REPLIES['text']:
            self.__reply_text(msg, msg['text'])
        else:
            # If not, reply to the user that the text is unknown
            self.__reply_text(msg, Text.UNKNOWN)

    # pylint: disable=E1121, R0911,R0912
    def __handle_photo_message(self, msg):
        """
        Parse a photo and it's commands, process the image, and reply the results

        :param msg: Required. The original message from the user.
        """

        # Does the message have a caption (where the commands are)
        if 'caption' in msg:
            # parse the commands
            commands = CaptionParser.parse(msg['caption'].lower())

            # If no commands are found in the caption,
            # it is considered to have no caption
            if len(commands) == 0 or isinstance(commands[0], NoCaptionError):
                # Reply with no caption error
                self.__reply_error(msg, ErrorTypes.NO_CAPTION)
                return

            # Handle errors in the commands.
            if self.__handle_command_errors(msg, commands):
                # If any error found, stop the photo handling process
                return

            # Fetch all multi-image commands
            multies = []
            for command in commands:
                if command.multi:
                    multies.append(command.command_name)

            # Check and handle the multi-image command amount
            if self.__handle_multies_errors(msg, multies):
                # If found and handle multi-image error,
                # stop the photo handling process
                return

            # Check and handle the arg errors
            if self.__handle_args_errors(msg, commands):
                # Stop the photo handling process if arg errors found
                return

            # If this message is a part of a multi-image command,
            # cache the message, and wait for the next image,
            # to process them both
            if len(multies) == 1 and 'media_group_id' in msg:
                msg['commands'] = commands
                self.cache[msg['from']['id']] = msg
                return

            # Notify the user that the request is accepted and is starting image processing
            self.__reply_text(msg, Photo.PROCESSING, category='photo')

            # Process the image according to the commands in the caption
            result_path, [source_img] = self.__process_image([msg], commands)
            # Reply the resulting image
            self.__reply_photo(msg, result_path)

            # Delete all related images from storage
            source_img.delete()
            source_img.path = result_path
            source_img.delete()

        # If message do not have caption
        else:
            # extract user ID for convenience
            user_id = msg['from']['id']
            # Verify that the current image is grouped with the previous photo message
            if (user_id in self.cache
                    and 'caption' in self.cache[user_id]
                    and 'media_group_id' in msg
                    and 'media_group_id' in self.cache[user_id]
                    and msg['media_group_id'] == self.cache[user_id]['media_group_id']):

                # extract cached message for convenience
                cached_msg = self.cache[user_id]

                # If the cached message is marked as used, ignore the current message
                if 'used' in cached_msg:
                    return

                # If the cached message does not have caption, reply with a no caption error
                if 'commands' not in self.cache[user_id] or not self.cache[user_id]['commands']:
                    self.__reply_error(msg, ErrorTypes.NO_CAPTION)
                    return

                # Notify the user that the request is accepted and is starting image processing
                self.__reply_text(msg, Photo.PROCESSING, category='photo')

                # Process the image according to the commands in the caption
                result_path, source_imgs = self.__process_image(
                    [cached_msg, msg], cached_msg['commands']
                )
                # Reply the resulting image
                self.__reply_photo(msg, result_path)
                # Delete all related images from storage
                for img in source_imgs:
                    img.delete()
                source_imgs[0].path = result_path
                source_imgs[0].delete()
                self.cache[user_id]['used'] = True

            # If there is no chached related message,
            # and there is no caption to the message,
            # reply with a no caption error
            else:
                self.__reply_error(msg, ErrorTypes.NO_CAPTION)
    # pylint: enable=E1121, R0911, R0912

    def __handle_command_errors(self, msg, commands):
        """
        Check and handle command error

        :param msg: Required. The original message from the user.
        :param commands: Required. The list of EffectCommands or CommandErrors,
               parsed from the message
        :return: True for error found and handled, or False for no error found
        """

        # Parse errors to error responses
        error_responses = []
        for command in commands:
            # If a command is a CommandError (has errors)
            if isinstance(command, CommandError):
                # parse the error to a response
                error_responses.append(
                    self.__parse_response(command.error_type, command.error_args)
                )

        # If got command errors, reply errors to the user
        if len(error_responses) > 0:
            self.__reply_error(msg, text = '\n'.join(error_responses))
            return True

        # else return False
        return False

    def __handle_multies_errors(self, msg, multies):
        """
        Check and handle multi-image effect amount error
        (Too many multi-image commands, or not enough images)

        :param msg: Required. The original message from the user.
        :param multies: Required. The list of the names of the
               multi-image effects given in the caption.
        :return: True for error found and handled, or False for no error found.
        """

        # If got multies
        if len(multies) > 0:
            # and if this message has no media group ID,
            # meaning this massage have no following massages
            # with more images
            if 'media_group_id' not in msg:
                # Reply with 'no second image' error
                self.__reply_error(msg, ErrorTypes.NO_2ND_IMAGE, [multies[0]])

                return True

            # If got more than 1 multies (not allowed)
            # reply with too much multies error.
            if len(multies) > 1:
                self.__reply_error(msg, ErrorTypes.TOO_MUCH_MULTI_IMAGE, ['\n'.join(multies)])

                # store the msg as used, so the other grouped images will be ignored
                msg['used'] = True
                self.cache[msg['from']['id']] = msg

                return True

        # else, no errors found
        return False

    def __handle_args_errors(self, msg, commands):
        """
        Check and handle arg errors
        :param msg: Required. The original message from the user.
        :param commands: Required. The list of EffectCommands or CommandErrors,
               parsed from the message
        :return:  True for error found and handled, or False for no error found.
        """

        # Fetch all arg errors
        commands_with_errors = []
        for command in commands:
            # In each command fetch all arg errors
            error_args_list = list(filter(
                lambda arg: isinstance(arg, CommandError),
                command.arg_list
            ))
            # append all arg errors into new list of commands
            if len(error_args_list) > 0:
                commands_with_errors.append(EffectCommand(error_args_list[0].error_args[0],
                                                          error_args_list))

        # If got arg errors
        if len(commands_with_errors) > 0:
            def parse_command_errors(command):
                """
                Internal functions, to parse all arg errors in a command, into a response

                :param command: Required. The command with errors.
                :return: The response as a string.
                """
                def parse_arg(arg):
                    """
                    Internal function to parse an arg error into a response
                    :param arg: Required. The arg error as CommandError
                    :return: The response as a string.
                    """

                    text = f'{
                        arg.error_args[-1] # The given value of the arg
                    }: {
                        # Parse the response
                        self.__parse_response(arg.error_type, arg.error_args)
                    }'

                    # Return the result
                    return text

                # Parse all args into a list of responses
                parsed_args = list(map(parse_arg, command.arg_list))

                # Parse the response of all args with the replies system
                # and return the result
                return self.__parse_response(
                    ErrorTypes.ARG_ERROR,
                    [
                        command.arg_list[0].error_args[0],
                        '\n'.join(parsed_args)
                ])

            # Parse all commands into a list
            parsed_responses = list(map(parse_command_errors, commands_with_errors))

            # Join all errors, and reply to the user
            self.__reply_error(msg, text = '\n\n'.join(parsed_responses))
            return True

        # else, no errors found
        return False

    def __process_image(self, msgs, commands):
        """
        Process the image according to the commands

        :param msgs: Required. The list of messages. Every message with a single photo.
        :param commands: Required. The list of EffectCommands, parsed from the caption.
        :return: The path of the resulting image
        """

        # Download all input images. Store and import them as Img instances
        imgs = list(map(lambda msg: Img(self.download_user_photo(msg)), msgs))

        # Image processing
        # Iterate over all commands
        for command_data in commands:
            # extract the method for processing command
            command = getattr(imgs[0], command_data.command_name)
            # If the command is a multi-image effect
            if command_data.multi:
                # insert the second image, and call the method for processing
                command(imgs[1], *command_data.arg_list)
            else:
                # With single image effects, call for processing without additional image
                command(*command_data.arg_list)

        return imgs[0].save_img(), imgs

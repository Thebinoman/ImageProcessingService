"""
Main file. Application starts here.
Initiate Flask application, and import imports.
"""

import os
import flask
from flask import request
# pylint: disable=W0611, E0401
from polybot.bot import Bot, QuoteBot, ImageProcessingBot
# pylint: enable=W0611, E0401

# Init Flask app
app = flask.Flask(__name__)

# Fetch Token from environment variables
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
# Fetch URL from environment variables
TELEGRAM_APP_URL = os.environ['TELEGRAM_APP_URL']


@app.route('/', methods=['GET'])
def index():
    """
    Does nothing. Returns 'Ok'
    :return: 'Ok' as a string when done
    """

    return 'Ok'


@app.route(f'/{TELEGRAM_TOKEN}/', methods=['POST'])
def webhook():
    """
    The webhook. Calling the bot to handle each message
    :return: 'Ok' as a string when done
    """

    # Convert request to JSON
    req = request.get_json()
    # Call the bot to handle the message
    bot.handle_message(req['message'])

    return 'Ok'


# If run as main file, run the app
if __name__ == "__main__":
    # Run the bot
    bot = ImageProcessingBot(TELEGRAM_TOKEN, TELEGRAM_APP_URL)

    # Run the app
    app.run(host='0.0.0.0', port=8443)

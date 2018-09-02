import json
import logging
import os
import sys
from dotenv import load_dotenv,find_dotenv
from telebot import TeleBot
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.yandex_api import yandex_diccionary
from src.telegram_object import TelegramMessageObject

load_dotenv(find_dotenv())
logger = logging.getLogger()
logger.setLevel(logging.INFO)

bot = TeleBot(os.getenv("telegram_token"))
yandex_object = yandex_diccionary(yandex_api_key=os.getenv("yandex_api_key"),
                                yandex_diccionary_key=os.getenv("yandex_diccionary"))
yandex_languages = yandex_object.get_all_available_languages(language_id='en')
yandex_translations = yandex_object.get_all_available_translations()


OK_RESPONSE = {"statusCode": 200, "headers": {}, "body": "Succesfull Requests"}
FAILED_RESPONSE = {"statusCode": 404, "headers": {}, 
                    "body": "Something goes wrong"}

def proccess_lambda_headers(headers, headers_key):
    python_string = headers.get(headers_key)
    if python_string:
        return json.loads(python_string.replace("'", ""))

def parse_translator(text):
    message_arguments = text.split(' ')
    if len(message_arguments) >= 2:
        target_language = message_arguments[0]
        message = ' '.join(message for message in message_arguments[1:])
        message_language = yandex_object.detect_language(message)
        message_translate = yandex_object.translate_message(message=message, 
                                            language_to_translate=target_language,
                                            message_language=message_language)
        if message_translate:
            return message_translate

def send_welcome(chat_id, message_id, message):
    bot.send_message(chat_id, "Welcome to translator")


def send_languages(message_id,chat_id, message):
    yandex_languages_text = ''.join(f'{key}––>{value}\n'
                                     for key, value in yandex_languages.items())

    bot.send_message(reply_to_message_id=message_id, chat_id=chat_id, 
                      text=yandex_languages_text)

def send_help(message_id,chat_id,message):
    help_message = f'Translate a message to the language you want, follow this steps:\n' \
                   f'\t\t 1.Choose your target translate language in the two digits code.\n' \
                   f'\t\t\t\t To see all the differents languages codes use /languages command.\n' \
                   f'\t\t\t\t To see all the available translations use /translations command.\n'\
                   f'\t\t 2.Write your message.\n' \
                   f'The message should follow the following structure LANGUAGECODE message.\n' \
                   f'just as an example: en eres tonto si estas utilizando este bot.'
    bot.send_message(reply_to_message_id=message_id, chat_id=chat_id, text=help_message)


def send_translation(message_id, chat_id, message):
    reply_message = ','.join(translation for translation in yandex_translations)
    bot.send_message(reply_to_message_id=message_id, chat_id=chat_id, 
                          text=reply_message)

def send_synonyms(message_id, chat_id, message):
    synonyms_input = message.split(' ')
    target_language = None
    target_message = message.split()[1:]
    if len(synonyms_input)>=3 and synonyms_input[1] in yandex_languages:
        target_language = synonyms_input[1]
        target_message  = synonyms_input[2:]
    input_message = ' '.join(word for word in target_message)
    synonyms = yandex_object.get_word_diccionary(text=input_message,
                                                language=target_language)
    if synonyms:
        reply_message = '\n'.join(synonym for synonym in synonyms)
        bot.send_message(reply_to_message_id=message_id, chat_id=chat_id,
                         text=reply_message)

def translate_message(message_id, chat_id, message):
    translate_message = parse_translator(message)
    if translate_message:
        bot.send_message(reply_to_message_id=message_id,chat_id=chat_id, 
                         text=translate_message)

def telegram_execute_method(message_id,chat_id, message):
    target_function = message.split(' ')[0]
    telegram_function =  {'/start': send_welcome,'/languages': send_languages,
                          '/translations': send_translation,'/help': send_help,
                          '/synonyms': send_synonyms
                          }.get(target_function, translate_message)

    telegram_function(message_id=message_id,chat_id=chat_id,message=message)

def telegram_trigger(event, context):
    logger.info("lambda event triggered")
    logger.info(f"{context}")
    logger.info(f"{event}")
    requests_body = proccess_lambda_headers(event, 'body')
    if not requests_body:
        logger.error("No body key")
    else:
        telegram_object = TelegramMessageObject(requests_body)
        if telegram_object:
            telegram_execute_method(message=telegram_object.text, 
                                    chat_id=telegram_object.chat_id,
                                    message_id=telegram_object.message_id)
            return OK_RESPONSE
    return FAILED_RESPONSE
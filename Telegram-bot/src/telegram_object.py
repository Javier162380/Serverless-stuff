import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import src.helpers as helpers

class TelegramMessageObject:
    def __init__(self,telegram_hash):
        self.update_id = telegram_hash['update_id']
        self.message_id = telegram_hash['message']['message_id']
        self.message_user_id = telegram_hash['message']['from']['id']
        self.message_is_bot = telegram_hash['message']['from']['is_bot']
        self.message_first_name = telegram_hash['message']['from']['first_name']
        self.chat_id = telegram_hash['message']['chat']['id']
        self.chat_first_name = telegram_hash['message']['chat']['first_name']
        self.chat_type = telegram_hash['message']['chat']['type']
        self.message_date = helpers.convert_unixtime_to_timestamp(
                            telegram_hash['message']['date'])
        self.text = telegram_hash['message']['text']
from requests import Session

class yandex_transaltor():

    def __init__(self,yandex_api_key):
        self.yandex_api_key = yandex_api_key
        self.session = Session()

    @staticmethod
    def truncate_message(message, max_limit=10000):
        return message[:max_limit]

    def detect_language(self, message, max_limit=10000):
        lang_detection = self.session.post(f'https://translate.yandex.net/api/v1.5/tr.json/detect'
                                           f'?key={self.yandex_api_key}'
                                           f'&text={self.truncate_message(message, max_limit)}')
        if lang_detection.status_code == 200:
            return lang_detection.json()['lang']

    def get_languages(self, language_id=None):
        language_end_point = f'https://translate.yandex.net/api/v1.5/tr.json/getLangs?key={self.yandex_api_key}'
        if language_id:
            language_end_point = f'{language_end_point}&ui={language_id}'
        languages = self.session.get(language_end_point)
        if languages.status_code == 200:
            return languages.json()

    def get_all_available_languages(self, language_id):
        languages_information = self.get_languages(language_id=language_id)
        if languages_information:
            return languages_information['langs'] if 'langs' in languages_information.keys() else None

    def get_all_available_translations(self, language_id=None):
        languages_information = self.get_languages(language_id=language_id)
        if languages_information:
            return languages_information['dirs'] if 'dirs' in languages_information.keys() else None

    def translate_message(self, message, language_to_translate, message_language):
        translate_message = self.session.post(f'https://translate.yandex.net/api/v1.5/tr.json/translate'
                                              f'?key={self.yandex_api_key}'
                                              f'&text={self.truncate_message(message)}'
                                              f'&lang={message_language}-{language_to_translate}')
        if translate_message.status_code == 200:
            return translate_message.json()['text']
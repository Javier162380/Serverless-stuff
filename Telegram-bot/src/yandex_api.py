from requests import Session

class yandex_transaltor:

    def __init__(self,yandex_api_key):
        self.yandex_api_key = yandex_api_key
        self.session = Session()

    @staticmethod
    def truncate_message(message, max_limit=10000):
        return message[:max_limit]

    def detect_language(self, message, max_limit=10000):
        data = {'key': self.yandex_api_key,
                'text': self.truncate_message(message, max_limit)}
        lang_detection = self.session.post('https://translate.yandex.net/api/'
                                           'v1.5/tr.json/detect', data=data)
        if lang_detection.status_code == 200:
            return lang_detection.json()['lang']

    def get_languages(self, language_id=None):
        language_end_point = f'https://translate.yandex.net/api/v1.5/tr.json/'\
                            f'getLangs?key={self.yandex_api_key}'
        if language_id:
            language_end_point = f'{language_end_point}&ui={language_id}'
        languages = self.session.get(language_end_point)
        if languages.status_code == 200:
            return languages.json()

    def get_all_available_languages(self, language_id):
        languages_information = self.get_languages(language_id=language_id)
        if languages_information:
            return languages_information['langs'] 
                    if 'langs' in languages_information.keys() else None

    def get_all_available_translations(self, language_id=None):
        languages_information = self.get_languages(language_id=language_id)
        if languages_information:
            return languages_information['dirs'] 
                if 'dirs' in languages_information.keys() else None

    def translate_message(self, message, language_to_translate, message_language):
        data = {'key':self.yandex_api_key, 'text':self.truncate_message(message),
                'lang':f"{message_language}-{language_to_translate}"}
        translate_message = self.session.post('https://translate.yandex.net/'
                                              'api/v1.5/tr.json/translate',
                                               data=data)
        if translate_message.status_code == 200:
            return translate_message.json()['text']

class yandex_diccionary(yandex_transaltor):

    def __init__(self,yandex_api_key, yandex_diccionary_key):
        self.yandex_api_key = yandex_api_key
        self.yandex_diccionary_key = yandex_diccionary_key
        self.session = Session()

    def get_word_diccionary(self, text, language=None):
        target_language = self.detect_language(message=text)
        data = {"key": self.yandex_diccionary_key,
                "text": self.truncate_message(text)}
        target_language = self.detect_language(text)
        if language:
            data['lang']=f"{language}-{target_language}"
        else:
            data['lang']=f"{target_language}-{target_language}"
        diccionary_end_point = self.session.post("https://dictionary.yandex."
                                                 "net/api/v1/dicservice.json/"
                                                 "lookup", data=data)
        synonyms = diccionary_end_point.json()['def'][0] 
                 if len(diccionary_end_point.json()['def']) else None
        if synonyms:
            return [synonym['text'] for synonym in synonyms['tr']]
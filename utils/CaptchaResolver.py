from loguru import logger
import requests


class CaptchaResolver(object):

    def __init__(self, api_url="https://api.yescaptcha.com/createTask",
                 api_key="0656d6736dffece2a634838ff6c252091a31e4c017209"):
        self.api_url = api_url
        self.api_key = api_key

    def create_task(self, queries, question):
        logger.debug(f'start to recognize image for question {question}')
        data = {
            "clientKey": self.api_key,
            "task": {
                "type": "HCaptchaClassification",
                "queries": queries,
                "question": question
            }
        }
        try:
            response = requests.post(self.api_url, json=data)
            result = response.json()
            logger.debug(f'captcha recogize result {result}')
            return result
        except requests.RequestException:
            logger.exception(
                'error occurred while recognizing captcha', exc_info=True)

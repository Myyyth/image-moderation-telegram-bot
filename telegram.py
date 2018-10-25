import requests
import json


class TelegramBot:
    """
    Wrapper for Telegram API, v0.1
    """
    TOKEN = ''
    BASIC_API_URL = ''
    FILE_API_URL = ''
    UPDATES_OFFSET = 0
    PROXY = {}

    def __init__(self, token):
        self.TOKEN = token
        self.BASIC_API_URL = 'https://api.telegram.org/bot{0}/'.format(token)
        self.FILE_API_URL = 'https://api.telegram.org/file/bot{0}/'.format(token)

    def set_proxy(self, ip, port):
        """
        Sets proxy for accessing Telegram API if client have trouble with an access to 'api.telegram.org'
        Proxy should support HTTP/S
        :param ip: ip of the proxy server
        :param port: port of the proxy server
        """
        proxy = "{0}:{1}".format(ip, port)
        self.PROXY['https'] = proxy

    def get_me(self):
        """
        Test function for Telegram API
        :return: information about bot
        """
        if 'https' in self.PROXY:
            response = requests.get(self.BASIC_API_URL + "getMe", proxies=self.PROXY)
        else:
            response = requests.get(self.BASIC_API_URL + "getMe")
        return json.loads(response.content.decode('utf-8'))

    def get_updates(self, use_offset=True):
        """
        Getting all new messages, where the bot is present. Used with long polling
        :param use_offset: if True, deletes all read messages from updates
        :return: JSONed content from Telegram API for 'getUpdates' method
        """
        if use_offset:
            data = {'offset': self.UPDATES_OFFSET}
            if 'https' in self.PROXY:
                response = requests.get(self.BASIC_API_URL + "getUpdates", params=data, proxies=self.PROXY)
            else:
                response = requests.get(self.BASIC_API_URL + "getUpdates", params=data)
        else:
            if 'https' in self.PROXY:
                response = requests.get(self.BASIC_API_URL + "getUpdates", proxies=self.PROXY)
            else:
                response = requests.get(self.BASIC_API_URL + "getUpdates")
        jsoned = json.loads(response.content.decode('utf-8'))
        if jsoned['ok']:
            if jsoned['result']:
                self.UPDATES_OFFSET = jsoned['result'][-1]['update_id'] + 1
        return jsoned

    def get_file(self, file_id):
        """
        Gets the file path
        :param file_id: id of the file
        :return: JSONed content from Telegram API for 'getFile' method
        """
        if 'https' in self.PROXY:
            response = requests.get(self.BASIC_API_URL + "getFile", params={'file_id': file_id}, proxies=self.PROXY)
        else:
            response = requests.get(self.BASIC_API_URL + "getFile", params={'file_id': file_id})
        return json.loads(response.content.decode('utf-8'))

    def download_file(self, file_path):
        """
        Downloads file from Telegram Server
        :param file_path: path to the file. See 'getFile' method in the API to know the details
        :return: raw bytes of the file
        """
        if 'https' in self.PROXY:
            response = requests.get(self.FILE_API_URL + file_path, proxies=self.PROXY)
        else:
            response = requests.get(self.FILE_API_URL + file_path)
        return response.content

    def send_message(self, chat_id, text):
        """
        Sends message to the chat
        :param chat_id: chat id where message should be sent
        :param text: text to be sent
        :return: JSONed content from Telegram API for 'sendMessage' method
        """
        data = {'chat_id': chat_id, 'text': text}
        if 'https' in self.PROXY:
            response = requests.get(self.BASIC_API_URL + "sendMessage", params=data, proxies=self.PROXY)
        else:
            response = requests.get(self.BASIC_API_URL + "sendMessage", params=data)
        return json.loads(response.content.decode('utf-8'))


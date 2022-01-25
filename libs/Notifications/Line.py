import requests
import os

class Line:
    def __init__(self):
        self.__VERSION__ = '0.1b'


    def notifications(self, msg):
        print(f"Send message: {msg} v: {self.__VERSION__}")
        url = "https://notify-api.line.me/api/notify"
        payload = f"message={msg}"
        headers = {
            'Authorization': f"Bearer {os.getenv('API_LINE_NOTIFICATION')}",
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request(
            "POST", url, headers=headers, data=payload.encode('utf-8'))

        print(f"line status => {response}")
        if response.status_code == 200:
            return True

        return False
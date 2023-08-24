


import requests
from .my_pass import tg_token,chat_id


class telega_bot():

    def tg_sender(message):

                try:
                    url = f"https://api.telegram.org/bot{tg_token}/sendMessage?chat_id={chat_id}&text={message}"
                    requests.get(url).json()
                except ValueError:
                    print("Error send message")
                return print("tg_sender is ok")


if __name__ == '__main__':
        message = 'test'
        tgbot = telega_bot()
        tgbot.tg_sender(message)



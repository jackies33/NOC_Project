


import requests
import argparse
import datetime

parser = argparse.ArgumentParser()
parser.add_argument("--db_type")
args = parser.parse_args()
db = args.db_type

class telega_bot():

    from my_pass import tg_token, chat_id
    """
    Class for telegram bot , send messages
    """

    def tg_sender(self,*args):

                message = f"Backup {db} was successful in {datetime.datetime.now()}"
                try:
                    url = f"https://api.telegram.org/bot{self.tg_token}/sendMessage?chat_id={self.chat_id}&text={message}"
                    requests.get(url).json()
                except ValueError:
                    print("Error send message")
                return print("tg_sender is ok")


if __name__ == "__main__":
    sender = telega_bot()
    sender.tg_sender()




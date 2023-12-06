import time
import configparser
import json

from telethon.sync import TelegramClient
from telethon import connection, functions

from datetime import date, datetime

from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import ChannelParticipantsSearch

from telethon.tl.functions.messages import GetHistoryRequest


# class for parsing data from telegram channels
class TelegramChannel:
    url = ""
    frequency = 60

    def __init__(self, url, frequency):
        self.url = url
        self.frequency = frequency

    def request(self, client):
        channel = client.get_entity(self.url)
        with client:
            result = client(functions.channels.GetMessagesRequest(
                channel=channel,
                id=[0]))
            print(result.stringify())

    def parse(self):
        pass

    def run(self, client):
        while True:
            self.request(client)
            self.parse()
            time.sleep(self.frequency)

import configparser
import datetime
from time import sleep

from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest

from model.Config import TELEGRAM_CHANNELS, REQUEST_FREQUENCY, KEYWORDS
from model.TelegramChannel import TelegramChannel


def auth_client():
    config = configparser.ConfigParser()
    config.read("config.ini")
    api_id = config['Telegram']['api_id']
    api_hash = config['Telegram']['api_hash']
    username = config['Telegram']['username']
    return TelegramClient(username, api_id, api_hash, system_version="4.16.30-vxCUSTOM")


client = auth_client()
client.connect()
if not client.is_user_authorized():
    client.start()

ACCIDENT_KEYWORDS = KEYWORDS.split(",")
CHAT_TO_FORWARD = client.get_entity('Ilyin_ad')


def init_channels():
    channels = dict()
    for channel_name in TELEGRAM_CHANNELS.split(','):
        channel = TelegramChannel("t.me/" + channel_name, REQUEST_FREQUENCY)
        channels[channel.url] = channel
    return channels


def dump_unread_messages(channel_id, unread_count):
    limit_msg = unread_count  # максимальное число записей, передаваемых за один раз
    all_messages = []  # список всех сообщений
    total_count_limit = unread_count
    while True:
        history = client(GetHistoryRequest(
            peer=client.get_entity(channel_id),
            offset_id=0,
            offset_date=None, add_offset=0,
            limit=limit_msg, max_id=0, min_id=0,
            hash=0))
        if not history.messages:
            break
        messages = history.messages
        for message in messages:
            all_messages.append(message)
        total_messages = len(all_messages)
        if total_count_limit != 0 and total_messages >= total_count_limit:
            break
    return all_messages


def get_unread_messages(dialogs):
    print("scanning for unread messages...")
    new_messages = dict()
    for dialog in dialogs:
        if dialog.is_channel:
            unread_count = dialog.dialog.unread_count
            if unread_count > 0:
                sleep(1)
                channel_id = dialog.dialog.peer.channel_id
                unread_messages = dump_unread_messages(channel_id, unread_count)
                client.send_read_acknowledge(dialog)
                new_messages[dialog] = unread_messages
    return new_messages


def message_contain_accident(message):
    if message.message is not None and len(message.message) > 0:
        message_words = tokenize_message(message.message)
        for message_word in message_words:
            if message_word in ACCIDENT_KEYWORDS:
                return True
    return False


def tokenize_message(message_text):
    words = message_text.split()
    words = [word.replace('\n', '').lower() for word in words]
    return words


def main():
    dialogs = client.get_dialogs()
    unread_messages_from_channel = get_unread_messages(dialogs)
    accident_messages = []
    print("searching for accidents...")
    for channel, messages in unread_messages_from_channel.items():
        for message in messages:
            if message_contain_accident(message):
                accident_messages.append(message)
    if len(accident_messages) > 0:
        print('Found', len(accident_messages), 'accidents, forwarding...')
        client.forward_messages(CHAT_TO_FORWARD, accident_messages)
        print('successfully sent, waiting', REQUEST_FREQUENCY, 'seconds')
    else:
        print('no accidents, waiting', REQUEST_FREQUENCY, 'seconds')


for i in range(30):
    print(datetime.datetime.now(), "going for scrape...")
    main()
    sleep(REQUEST_FREQUENCY)

client.disconnect()

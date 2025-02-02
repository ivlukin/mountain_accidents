import configparser

from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
import json
from time import sleep


# Введите свои данные

def auth_client():
    config = configparser.ConfigParser()
    config.read("config.ini")
    api_id = config['Telegram']['api_id']
    api_hash = config['Telegram']['api_hash']
    username = config['Telegram']['username']
    return TelegramClient(username, api_id, api_hash, system_version="4.16.30-vxCUSTOM")

client = auth_client()
client.start()
channel_username = 'Mountain_Accidents'

# Имя файла для сохранения сообщений
output_file = 'messages.json'

# Создаем клиент


async def main():

    # Получаем информацию о канале
    channel = await client.get_entity(channel_username)

    # Получаем все сообщения из канала
    all_messages = []
    offset_id = 0
    limit = 100
    total_count_limit = 0  # Установите лимит, если хотите ограничить количество сообщений

    while True:
        history = await client(GetHistoryRequest(
            peer=channel,
            offset_id=offset_id,
            offset_date=None,
            add_offset=0,
            limit=limit,
            max_id=0,
            min_id=0,
            hash=0
        ))
        if not history.messages:
            break
        messages = history.messages
        for message in messages:
            # Сохраняем только нужные данные
            message_data = {
                'id': message.id,
                'date': message.date.isoformat(),
                'text': message.message,
            }
            all_messages.append(message_data)
        offset_id = messages[-1].id
        if total_count_limit != 0 and len(all_messages) >= total_count_limit:
            break
        sleep(5)

    # Сохраняем сообщения в JSON-файл
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_messages, f, ensure_ascii=False, indent=4)

    print(f"Сообщения сохранены в файл: {output_file}")

    # Закрываем клиент
    await client.disconnect()


# Запускаем клиент
with client:
    client.loop.run_until_complete(main())
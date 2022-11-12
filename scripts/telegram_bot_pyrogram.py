#!/usr/bin/python3
import asyncio
import uvloop
from pyrogram import Client, filters
import os

base_folder = os.path.join(os.path.dirname(__file__), '..')
data_path = os.path.join(base_folder, 'data')
local_csv_path = os.path.join(data_path, 'mobile-phone-data.csv')
os.makedirs(data_path, exist_ok=True)

api_id = 25775
api_hash = "2e67c1b097b2519240dc94e0d384c19a"

app = Client("my_telegram_bot", api_id, api_hash)


@app.on_message(filters.text & filters.private)
async def text_handler(client, message):
    await message.reply(message.text)


@app.on_message(filters.document)
async def document_handler(client, message):
    print(message)
    if message.document.mime_type not in ('text/csv', 'text/comma-separated-values'):
        await message.reply('Not a CSV file')

    file_name = message.document.file_name
    file_in_mem = await app.download_media(message, in_memory=True)
    file_bytes = bytes(file_in_mem.getbuffer())

    with open(local_csv_path, 'wb') as new_file:
        new_file.write(file_bytes)
        print('Written into ' + local_csv_path)

    original_file = os.path.join(data_path, file_name)
    with open(original_file, 'wb') as new_file:
        new_file.write(file_bytes)
        print('Written into ' + original_file)

    await message.reply('Trace file ' + file_name + ' is saved')


app.run()

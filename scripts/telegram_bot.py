#!/usr/bin/python3
import telebot
import os

base_folder = os.path.join(os.path.dirname(__file__), '..')
local_csv_path = os.path.join(base_folder, 'data', 'mobile-phone-data.csv')
os.makedirs(os.path.dirname(local_csv_path), exist_ok=True)

bot = telebot.TeleBot("5390413555:AAHYXYupDKq9-uXwxASJCsMrSDaeagU5ys8", parse_mode=None)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    print('Received a message')
    print(message)
    bot.reply_to(message, message.text)

@bot.message_handler(content_types=['document'])
def handle_docs(message):
    print('Received a document')
    print(message)
    if message.document.mime_type not in ('text/csv', 'text/comma-separated-values'):
        bot.reply_to(message, 'Not a CSV file')
        return
    try:
        file_info = bot.get_file(message.document.file_id)
        print(file_info)
        downloaded_file = bot.download_file(file_info.file_path)
        new_file = open(local_csv_path, 'wb')
        new_file.write(downloaded_file)
        new_file.close()
        bot.reply_to(message, 'The trace file is saved')
    except Exception as e:
        print(e)
        bot.reply_to(message, 'Failed to save trace file: ' + str(e))

print('Start polling...')
bot.infinity_polling()

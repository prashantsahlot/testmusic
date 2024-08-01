Here is the complete code:


import telebot
from telebot import types
from pytube import YouTube, Search
import os

TOKEN = '7186451521:AAGUsHk2NNIw5BZQJVbqpEjzYOkcdam5QbI'

bot = telebot.TeleBot(TOKEN)

START_IMAGE_LINK = '(link unavailable)'
START_MENU_TEXT = ("Hello there! I'm a song downloading bot with the following commands:\n\n"
                   "🔍 Use /search to download youtube video or song \n"
                   " For example, send:\n"
                   " /search royalty")

@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_photo((link unavailable), START_IMAGE_LINK, caption=START_MENU_TEXT)

@bot.message_handler(commands=['search'])
def search(message):
    try:
        query = message.text.split(' ', 1)[1]
        search_results = Search(query).results
        if search_results:
            keyboard = types.InlineKeyboardMarkup()
            for result in search_results[:5]:  # Show top 5 results
                keyboard.add(types.InlineKeyboardButton(text=result.title, callback_data=f"video {result.watch_url}"))
            bot.send_message((link unavailable), "Choose a video:", reply_markup=keyboard)
        else:
            bot.reply_to(message, "No results found.")
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        command, data = call.data.split(' ', 1)
        if command == "video":
            download_video(call.message, data)
    except Exception as e:
        print(f"Error handling callback query: {e}")

def download_video(message, youtube_link):
    try:
        yt = YouTube(youtube_link)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        if stream:
            file_path = stream.download()
            with open(file_path, 'rb') as media_file:
                bot.send_video((link unavailable), media_file)
            os.remove(file_path)
        else:
            bot.reply_to(message, "No suitable stream found.")
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

bot.polling()

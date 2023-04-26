import os
import requests
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TOKEN = 'your_bot_token_here'

def start(update, context):
    keyboard = [
        ['TikTok', 'Instagram'],
        ['Facebook']
    ]
    reply_markup = telegram.ReplyKeyboardMarkup(keyboard)
    update.message.reply_text('Bitte wählen Sie die Plattform, von der Sie herunterladen möchten:', reply_markup=reply_markup)

def tiktok(update, context):
    chat_id = update.message.chat_id
    url = update.message.text
    try:
        r = requests.get(url)
        video_url = r.json()['video']['downloadAddr']
        file_name = 'tiktok_video.mp4'
        with open(file_name, 'wb') as f:
            f.write(requests.get(video_url).content)
        context.bot.send_video(chat_id=chat_id, video=open(file_name, 'rb'))
        os.remove(file_name)
    except:
        context.bot.send_message(chat_id=chat_id, text='Ein Fehler ist aufgetreten.')

def instagram(update, context):
    chat_id = update.message.chat_id
    url = update.message.text
    try:
        r = requests.get(url)
        shortcode = r.json()['graphql']['shortcode_media']['shortcode']
        video_url = r.json()['graphql']['shortcode_media']['video_url']
        file_name = f'{shortcode}.mp4'
        with open(file_name, 'wb') as f:
            f.write(requests.get(video_url).content)
        context.bot.send_video(chat_id=chat_id, video=open(file_name, 'rb'))
        os.remove(file_name)
    except:
        context.bot.send_message(chat_id=chat_id, text='Ein Fehler ist aufgetreten.')

def facebook(update, context):
    chat_id = update.message.chat_id
    url = update.message.text
    try:
        r = requests.get(url)
        video_url = r.text.split('hd_src:"')[1].split('",')[0]
        file_name = 'facebook_video.mp4'
        with open(file_name, 'wb') as f:
            f.write(requests.get(video_url).content)
        context.bot.send_video(chat_id=chat_id, video=open(file_name, 'rb'))
        os.remove(file_name)
    except:
        context.bot.send_message(chat_id=chat_id, text='Ein Fehler ist aufgetreten.')

def echo(update, context):
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id, text='Ungültige Eingabe. Bitte wählen Sie eine der verfügbaren Optionen.')

def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    dp.add_handler(MessageHandler(Filters.regex('^TikTok$'), tiktok))
    dp.add_handler(MessageHandler(Filters.regex('^Instagram$'), instagram))
    dp.add_handler(MessageHandler(Filters.regex('^Facebook$'), facebook))

    dp.add_handler(MessageHandler(Filters.text, echo))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()

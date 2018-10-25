import time
from telegram import TelegramBot

token = '726253065:AAFg-4Qs6JwT_B95peBC4t5iRX4UNeugOrc'


def respond_message(result):
    global bot
    if 'text' in result['message']:
        if result['message']['text'] == '/start':
            return 'Send me some NSFW image'
    elif 'photo' in result['message']:
        biggest_file_id = result['message']['photo'][len(result['message']['photo'])-1]['file_id']
        file = bot.get_file(biggest_file_id)
        if file['ok']:
            file = bot.download_file(file['result']['file_path'])
            # TODO: Upload 'file' to aws rekognition and check if it NSFW
            return 'That\'s a cool pic'
    return 'I don\'t know what you mean'


bot = TelegramBot(token)
# Remove or change proxy (depends on your connection)
bot.set_proxy('138.117.176.10', '46355')
while True:
    time.sleep(5)
    response = bot.get_updates(use_offset=True)
    if response['ok']:
        if response['result']:
            for result in response['result']:
                bot.send_message(result['message']['chat']['id'], respond_message(result))


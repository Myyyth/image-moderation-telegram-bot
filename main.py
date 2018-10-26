import time
import boto3
from telegram import TelegramBot

token = '726253065:AAFg-4Qs6JwT_B95peBC4t5iRX4UNeugOrc'
bot = TelegramBot(token)
rekognition = boto3.client('rekognition',
                           aws_access_key_id='AKIAI6EQBKCSDCWR66QQ',
                           aws_secret_access_key='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')


def detect_explicit_content(image_bytes):
    """ Checks image for explicit or suggestive content using Amazon Rekognition Image Moderation.
    Args:
        image_bytes (bytes): Blob of image bytes.
    Returns:
        (boolean)
        True if Image Moderation detects explicit or suggestive content in blob of image bytes.
        False otherwise.
    """
    global rekognition
    try:
        response = rekognition.detect_moderation_labels(
            Image={
                'Bytes': image_bytes,
            },
        )
    except Exception as e:
        raise e
    labels = response['ModerationLabels']
    if not labels:
        return False
    return True


def respond_message(result):
    global bot
    if 'text' in result['message']:
        print('Found some text, responding')
        if result['message']['text'] == '/start':
            return 'Send me some NSFW image'
    elif 'photo' in result['message']:
        print('Found some photo, responding')
        biggest_file_id = result['message']['photo'][len(result['message']['photo'])-1]['file_id']
        file = bot.get_file(biggest_file_id)
        if file['ok']:
            file = bot.download_file(file['result']['file_path'])
            is_explicit = detect_explicit_content(file)
            if is_explicit:
                return 'HOLY SHEAT THIS IS SOME FREAKIN NSFW PICTURE'
            else:
                return 'Good pic!'
    return 'I don\'t know what you mean'


# Remove or change proxy (depends on your connection)
bot.set_proxy('159.65.130.145', '80')
while True:
    try:
        time.sleep(1)
        print('Trying to fetch some new messages')
        response = bot.get_updates(use_offset=True)
        if response['ok']:
            if response['result']:
                print('Found new messages! Processing...')
                for result in response['result']:
                    bot.send_message(result['message']['chat']['id'], respond_message(result))
            else:
                print('No new messages')
    except Exception as e:
        print("===START_ERROR===")
        print(e)
        print("===END_ERROR===")

import boto3
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
EXPLICIT_MIN_CONFIDENCE = 0.5
TELEGRAM_TOKEN = '726253065:AAFg-4Qs6JwT_B95peBC4t5iRX4UNeugOrc'
REQUEST_KWARGS = {
    'proxy_url': 'http://159.65.130.145:80/'
}
rekognition = boto3.client('rekognition',
                           aws_access_key_id='AKIAI6EQBKCSDCWR66QQ',
                           aws_secret_access_key='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')
updater = Updater(token=TELEGRAM_TOKEN, request_kwargs=REQUEST_KWARGS)
dispatcher = updater.dispatcher


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Send me some NSFW image')


def set_confidence(bot, update):
    # TODO: Update local var
    bot.send_message(chat_id=update.message.chat_id, text='Confidence level updated')


def check_photo(bot, update):
    file_id = update.message.photo[-1].file_id
    file = bot.getFile(file_id).download_as_bytearray()
    is_explicit = detect_explicit_content(file)
    if is_explicit:
        bot.send_message(chat_id=update.message.chat_id, text='HOLY SHEAT THAT SOME NSFW IMAGE!')
    else:
        bot.send_message(chat_id=update.message.chat_id, text='All is fine :)')


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
            MinConfidence=EXPLICIT_MIN_CONFIDENCE
        )
    except Exception as e:
        raise e
    labels = response['ModerationLabels']
    if not labels:
        return False
    return True


dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('setconfidence', set_confidence))
dispatcher.add_handler(MessageHandler(Filters.photo, check_photo))
updater.start_polling()

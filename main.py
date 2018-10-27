import boto3
import logging
import sqlite3
import configparser
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram

bot_settings = configparser.ConfigParser()
bot_settings.read('bot_settings.ini')

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

TELEGRAM_TOKEN = str(bot_settings['telegram']['BotApiToken'])
REQUEST_KWARGS = {
    'proxy_url': 'http://{0}/'.format(str(bot_settings['telegram']['Proxy']))
}
rekognition = boto3.client('rekognition',
                           aws_access_key_id=str(bot_settings['amazon']['AccessKey']),
                           aws_secret_access_key=str(bot_settings['amazon']['SecretAccessKey']))
updater = Updater(token=TELEGRAM_TOKEN, request_kwargs=REQUEST_KWARGS)
dispatcher = updater.dispatcher


def init_new(chat_id):
    conn = sqlite3.connect('user_settings.db')
    cursor = conn.cursor()
    cursor.execute('SELECT chat_id FROM aws_image_settings WHERE chat_id = ?', (chat_id,))
    exists = cursor.fetchone()
    if exists:
        cursor.execute('UPDATE aws_image_settings SET confidence_level = 50, allow_nudity = 0, allow_male_nudity = 0, '
                       'allow_female_nudity = 0, allow_sexual_activity = 0, allow_partial_activity = 0, '
                       'allow_female_suit = 0, allow_male_suit = 0, allow_revealing_clothes = 0')
    else:
        cursor.execute('INSERT INTO aws_image_settings VALUES (?, 50, 0, 0, 0, 0, 0, 0, 0, 0)', (chat_id,))
    conn.commit()


def update_confidence_level(chat_id, confidence_level):
    conn = sqlite3.connect('user_settings.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE aws_image_settings SET confidence_level = ? WHERE chat_id = ?',
                   (confidence_level, chat_id))
    conn.commit()
    conn.close()


def update_nudity(chat_id, nudity):
    conn = sqlite3.connect('user_settings.db')
    cursor = conn.cursor()
    nudity = bool(nudity)
    if nudity:
        nudity = 1
    else:
        nudity = 0
    cursor.execute('UPDATE aws_image_settings SET allow_nudity = ? WHERE chat_id = ?',
                   (nudity, chat_id))
    conn.commit()
    conn.close()


def update_male_nudity(chat_id, male_nudity):
    conn = sqlite3.connect('user_settings.db')
    cursor = conn.cursor()
    male_nudity = bool(male_nudity)
    if male_nudity:
        male_nudity = 1
    else:
        male_nudity = 0
    cursor.execute('UPDATE aws_image_settings SET allow_male_nudity = ? WHERE chat_id = ?',
                   (male_nudity, chat_id))
    conn.commit()
    conn.close()


def update_female_nudity(chat_id, female_nudity):
    conn = sqlite3.connect('user_settings.db')
    cursor = conn.cursor()
    female_nudity = bool(female_nudity)
    if female_nudity:
        female_nudity = 1
    else:
        female_nudity = 0
    cursor.execute('UPDATE aws_image_settings SET allow_female_nudity = ? WHERE chat_id = ?',
                   (female_nudity, chat_id))
    conn.commit()
    conn.close()


def update_sexual_activity(chat_id, sexual_activity):
    conn = sqlite3.connect('user_settings.db')
    cursor = conn.cursor()
    sexual_activity = bool(sexual_activity)
    if sexual_activity:
        sexual_activity = 1
    else:
        sexual_activity = 0
    cursor.execute('UPDATE aws_image_settings SET allow_sexual_activity = ? WHERE chat_id = ?',
                   (sexual_activity, chat_id))
    conn.commit()
    conn.close()


def update_partial_activity(chat_id, partial_activity):
    conn = sqlite3.connect('user_settings.db')
    cursor = conn.cursor()
    partial_activity = bool(partial_activity)
    if partial_activity:
        partial_activity = 1
    else:
        partial_activity = 0
    cursor.execute('UPDATE aws_image_settings SET allow_partial_activity = ? WHERE chat_id = ?',
                   (partial_activity, chat_id))
    conn.commit()
    conn.close()


def update_female_suit(chat_id, female_suit):
    conn = sqlite3.connect('user_settings.db')
    cursor = conn.cursor()
    female_suit = bool(female_suit)
    if female_suit:
        female_suit = 1
    else:
        female_suit = 0
    cursor.execute('UPDATE aws_image_settings SET allow_female_suit = ? WHERE chat_id = ?',
                   (female_suit, chat_id))
    conn.commit()
    conn.close()


def update_male_suit(chat_id, male_suit):
    conn = sqlite3.connect('user_settings.db')
    cursor = conn.cursor()
    male_suit = bool(male_suit)
    if male_suit:
        male_suit = 1
    else:
        male_suit = 0
    cursor.execute('UPDATE aws_image_settings SET allow_male_suit = ? WHERE chat_id = ?',
                   (male_suit, chat_id))
    conn.commit()
    conn.close()


def update_revealing_clothes(chat_id, revealing_clothes):
    conn = sqlite3.connect('user_settings.db')
    cursor = conn.cursor()
    revealing_clothes = bool(revealing_clothes)
    if revealing_clothes:
        revealing_clothes = 1
    else:
        revealing_clothes = 0
    cursor.execute('UPDATE aws_image_settings SET allow_revealing_clothes = ? WHERE chat_id = ?',
                   (revealing_clothes, chat_id))
    conn.commit()
    conn.close()


def user_settings_to_telegram_text(settings):
    rez = ''
    for k, v in settings.items():
        rez += '*{0}*: {1}\n'.format(k, v)
    return rez


def get_user_settings(chat_id):
    conn = sqlite3.connect('user_settings.db')
    cursor = conn.cursor()
    settings = {}
    cursor.execute('SELECT * FROM aws_image_settings WHERE chat_id = ?', (chat_id,))
    rez = cursor.fetchone()
    conn.close()
    settings['Confidence level'] = rez[1]
    settings['Allow nudity'] = bool(rez[2])
    settings['Allow male nudity'] = bool(rez[3])
    settings['Allow female nudity'] = bool(rez[4])
    settings['Allow sexual activity'] = bool(rez[5])
    settings['Allow partial activity'] = bool(rez[6])
    settings['Allow female suit'] = bool(rez[7])
    settings['Allow male suit'] = bool(rez[8])
    settings['Allow revealing clothes'] = bool(rez[9])
    return settings


def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


def is_bool(string):
    try:
        bool(string)
        return True
    except ValueError:
        return False


def start(bot, update):
    init_new(update.message.chat_id)
    bot.send_message(chat_id=update.message.chat_id, text='Hello! As you ran /start command, I initialized all of your '
                                                          'setting to default. Please, refer to /help to customize')


def help(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='*Available commands*:\n\n'
                                                          '/start - Reinitialize the bot, settings are set to default\n'
                                                          '/help - Show this reference\n\n'
                                                          ' *Configure bot\'s settings*:\n'
                                                          ' /setconfidence [value] - Set confidence of explicit '
                                                          'content '
                                                          'to [value] (must be real number between 0 and 100). Default '
                                                          'value is 50\n'
                                                          ' /allownudity [value] - True for allowing nudity, False otherwise\n'
                                                          ' /allowfemalenudity [value] - True for allowing female nudity, False otherwise\n'
                                                          ' /allowmalenudity [value] - True for allowing male nudity, False otherwise\n'
                                                          ' /allowsexualactivity [value] - True for allowing sexual activity, False otherwise\n'
                                                          ' /allowpartialactivity [value] - True for allowing partialactivity, False otherwise\n'
                                                          ' /allowfemalesuit [value] - True for allowing female swimsuits, False otherwise\n'
                                                          ' /allowmalesuit [value] - True for allowing male suits, False otherwise\n'
                                                          ' /allowrevealingclothes [value] - True for allowing revealing clothes, False otherwise\n', parse_mode=telegram.ParseMode.MARKDOWN)


def pidor(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='@Stepan_Ustinov')


def settings(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=user_settings_to_telegram_text(
        get_user_settings(update.message.chat_id)) + '\nFor customizing settings, refer to /help',
                     parse_mode=telegram.ParseMode.MARKDOWN)


def set_confidence(bot, update, args):
    if len(args) == 0:
        bot.send_message(chat_id=update.message.chat_id, text='You haven\'t provided any value, refer to /help and try '
                                                              'again')
        return
    if len(args) > 1:
        bot.send_message(chat_id=update.message.chat_id, text='You have provided too much arguments (>1)')
        return
    if not is_float(args[0]):
        bot.send_message(chat_id=update.message.chat_id, text='You have provided wrong type for value. Use real number '
                                                              'instead')
        return
    if float(args[0]) < 0 or float(args[0]) > 100:
        bot.send_message(chat_id=update.message.chat_id, text='Value is not between 0 and 100')
        return
    update_confidence_level(update.message.chat_id, args[0])
    bot.send_message(chat_id=update.message.chat_id, text='Confidence level updated')


def allow_nudity(bot, update, args):
    if len(args) == 0:
        bot.send_message(chat_id=update.message.chat_id, text='You haven\'t provided any value, refer to /help and try '
                                                              'again')
        return
    if len(args) > 1:
        bot.send_message(chat_id=update.message.chat_id, text='You have provided too much arguments (>1)')
        return
    if not is_bool(args[0]):
        bot.send_message(chat_id=update.message.chat_id, text='You have provided wrong type for value. Use bool '
                                                              'instead')
        return
    update_nudity(update.message.chat_id, args[0])
    bot.send_message(chat_id=update.message.chat_id, text='Allow nudity updated')


def allow_female_nudity(bot, update, args):
    if len(args) == 0:
        bot.send_message(chat_id=update.message.chat_id, text='You haven\'t provided any value, refer to /help and try '
                                                              'again')
        return
    if len(args) > 1:
        bot.send_message(chat_id=update.message.chat_id, text='You have provided too much arguments (>1)')
        return
    if not is_bool(args[0]):
        bot.send_message(chat_id=update.message.chat_id, text='You have provided wrong type for value. Use bool '
                                                              'instead')
        return
    update_female_nudity(update.message.chat_id, args[0])
    bot.send_message(chat_id=update.message.chat_id, text='Female nudity updated')


def allow_male_nudity(bot, update, args):
    if len(args) == 0:
        bot.send_message(chat_id=update.message.chat_id, text='You haven\'t provided any value, refer to /help and try '
                                                              'again')
        return
    if len(args) > 1:
        bot.send_message(chat_id=update.message.chat_id, text='You have provided too much arguments (>1)')
        return
    if not is_bool(args[0]):
        bot.send_message(chat_id=update.message.chat_id, text='You have provided wrong type for value. Use bool '
                                                              'instead')
        return
    update_male_nudity(update.message.chat_id, args[0])
    bot.send_message(chat_id=update.message.chat_id, text='Male nudity updated')


def allow_sexual_activity(bot, update, args):
    if len(args) == 0:
        bot.send_message(chat_id=update.message.chat_id, text='You haven\'t provided any value, refer to /help and try '
                                                              'again')
        return
    if len(args) > 1:
        bot.send_message(chat_id=update.message.chat_id, text='You have provided too much arguments (>1)')
        return
    if not is_bool(args[0]):
        bot.send_message(chat_id=update.message.chat_id, text='You have provided wrong type for value. Use bool '
                                                              'instead')
        return
    update_sexual_activity(update.message.chat_id, args[0])
    bot.send_message(chat_id=update.message.chat_id, text='Sexual activity updated')


def allow_partial_activity(bot, update, args):
    if len(args) == 0:
        bot.send_message(chat_id=update.message.chat_id, text='You haven\'t provided any value, refer to /help and try '
                                                              'again')
        return
    if len(args) > 1:
        bot.send_message(chat_id=update.message.chat_id, text='You have provided too much arguments (>1)')
        return
    if not is_bool(args[0]):
        bot.send_message(chat_id=update.message.chat_id, text='You have provided wrong type for value. Use bool '
                                                              'instead')
        return
    update_partial_activity(update.message.chat_id, args[0])
    bot.send_message(chat_id=update.message.chat_id, text='Partial activity updated')


def allow_female_suit(bot, update, args):
    if len(args) == 0:
        bot.send_message(chat_id=update.message.chat_id, text='You haven\'t provided any value, refer to /help and try '
                                                              'again')
        return
    if len(args) > 1:
        bot.send_message(chat_id=update.message.chat_id, text='You have provided too much arguments (>1)')
        return
    if not is_bool(args[0]):
        bot.send_message(chat_id=update.message.chat_id, text='You have provided wrong type for value. Use bool '
                                                              'instead')
        return
    update_female_suit(update.message.chat_id, args[0])
    bot.send_message(chat_id=update.message.chat_id, text='Female suit updated')


def allow_male_suit(bot, update, args):
    if len(args) == 0:
        bot.send_message(chat_id=update.message.chat_id, text='You haven\'t provided any value, refer to /help and try '
                                                              'again')
        return
    if len(args) > 1:
        bot.send_message(chat_id=update.message.chat_id, text='You have provided too much arguments (>1)')
        return
    if not is_bool(args[0]):
        bot.send_message(chat_id=update.message.chat_id, text='You have provided wrong type for value. Use bool '
                                                              'instead')
        return
    update_male_suit(update.message.chat_id, args[0])
    bot.send_message(chat_id=update.message.chat_id, text='Male suit updated')


def allow_revealing_clothes(bot, update, args):
    if len(args) == 0:
        bot.send_message(chat_id=update.message.chat_id, text='You haven\'t provided any value, refer to /help and try '
                                                              'again')
        return
    if len(args) > 1:
        bot.send_message(chat_id=update.message.chat_id, text='You have provided too much arguments (>1)')
        return
    if not is_bool(args[0]):
        bot.send_message(chat_id=update.message.chat_id, text='You have provided wrong type for value. Use bool '
                                                              'instead')
        return
    update_revealing_clothes(update.message.chat_id, args[0])
    bot.send_message(chat_id=update.message.chat_id, text='Revealing clothes updated')


def check_sticker(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='I wish i could convert .webp to .png :(')


def check_photo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Processing your image...')
    file_id = update.message.photo[-1].file_id
    file = bot.getFile(file_id).download_as_bytearray()
    is_explicit = detect_explicit_content(update.message.chat_id, file)
    if is_explicit:
        bot.send_message(chat_id=update.message.chat_id, text='HOLY SHEAT THAT SOME NSFW IMAGE!')
    else:
        bot.send_message(chat_id=update.message.chat_id, text='All is fine :)')


def detect_explicit_content(chat_id, image_bytes):
    """ Checks image for explicit or suggestive content using Amazon Rekognition Image Moderation.
    Args:
        image_bytes (bytes): Blob of image bytes.
    Returns:
        (boolean)
        True if Image Moderation detects explicit or suggestive content in blob of image bytes.
        False otherwise.
    """
    global rekognition
    conn = sqlite3.connect('user_settings.db')
    cursor = conn.cursor()
    cursor.execute('SELECT confidence_level FROM aws_image_settings WHERE chat_id = ?', (chat_id,))
    confidence_level = cursor.fetchone()[0]
    conn.close()
    try:
        response = rekognition.detect_moderation_labels(
            Image={
                'Bytes': image_bytes,
            },
            MinConfidence=float(confidence_level)
        )
    except Exception as e:
        raise e
    labels = response['ModerationLabels']
    if not labels:
        return False
    return True


dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('setconfidence', set_confidence, pass_args=True))
dispatcher.add_handler(CommandHandler('allownudity', allow_nudity, pass_args=True))
dispatcher.add_handler(CommandHandler('allowmalenudity', allow_male_nudity, pass_args=True))
dispatcher.add_handler(CommandHandler('allowfemalenudity', allow_female_nudity, pass_args=True))
dispatcher.add_handler(CommandHandler('allowsexualactivity', allow_sexual_activity, pass_args=True))
dispatcher.add_handler(CommandHandler('allowpartialactivity', allow_partial_activity, pass_args=True))
dispatcher.add_handler(CommandHandler('allowfemalesuit', allow_female_suit, pass_args=True))
dispatcher.add_handler(CommandHandler('allowmalesuit', allow_male_suit, pass_args=True))
dispatcher.add_handler(CommandHandler('allowrevealingclothes', allow_revealing_clothes, pass_args=True))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(CommandHandler('pidor', pidor))
dispatcher.add_handler(CommandHandler('settings', settings))
dispatcher.add_handler(MessageHandler(Filters.photo, check_photo))
dispatcher.add_handler(MessageHandler(Filters.sticker, check_sticker))
updater.start_polling()

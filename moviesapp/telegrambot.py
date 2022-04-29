import telegram  # this is from python-telegram-bot package

from django.conf import settings
from django.template.loader import render_to_string


def post_event_on_telegram(event):
    message_html = render_to_string('moviesapp/telegram/send_to_telegram_channel.html', {
        'event': event
    })
    telegram_settings = settings.TELEGRAM
    bot = telegram.Bot(token=telegram_settings['bot_token'])
    bot.send_message(chat_id="@%s" % telegram_settings['channel_name'],
                     text=message_html, parse_mode=telegram.ParseMode.HTML)


def post_to_telegram_channel(template, context):
    message_html = render_to_string(template, context)
    telegram_settings = settings.TELEGRAM
    bot = telegram.Bot(token=telegram_settings['bot_token'])
    bot.send_message(chat_id="@%s" % telegram_settings['channel_name'],
                     text=message_html, parse_mode=telegram.ParseMode.HTML)

    if context["movie_image"]:
        bot.send_photo(chat_id="@%s" % telegram_settings['channel_name'], photo=open(context["movie_image"], 'rb'))

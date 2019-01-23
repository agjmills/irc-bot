from pyshorteners import Shortener
import re
import requests

def on_message(bot, channel, sender, message):
    if len(message.split()) == 0:
        message = "."
    for message_part in message.split():
        if message_part.startswith("http://") or message_part.startswith("https://"):
            get_url_title(channel, bot, message_part)


def get_url_title(channel, bot, url):
    if url.endswith('mp3') is False:
        html = requests.get(url).text
        title_match = re.search("<title>(.*?)</title>", html)
        try:
            shortener = Shortener('Isgd')
            short_url = shortener.short(url)
        except:
            short_url = None
    
        if title_match and short_url:
            bot.send_message(channel, "^ {} → {}".format(title_match.group(1), short_url))
            return
        if title_match and short_url is None:
            bot.send_message(channel, "^ {}".format(title_match.group(1)))
            return



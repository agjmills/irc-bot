#!/usr/bin/python3
# -*- coding: utf8 -*-
import JustIRC
import requests
import re
from pyshorteners import Shortener
import time
import yaml 
import sys

class Buttbot:
    configuration = {}
    bot = None

    def __init__(self):
        self.configure()
        self.setup_bot()

    def setup_bot(self):
        self.bot =  JustIRC.IRCConnection()
        self.bot.on_connect.append(self.on_connect)
        self.bot.on_welcome.append(self.on_welcome)
        self.bot.on_public_message.append(self.on_message)
        self.bot.connect("irc.freenode.net")
        self.bot.run_loop()
    
    def configure(self):
        with open("conf.yml", 'r') as stream:
            try:
                self.configuration = yaml.load(stream)
            except yaml.YAMLError as exception:
                print(exception)

    def on_connect(self, bot):
        bot.set_nick(self.configuration["nick"])
        bot.send_user_packet(self.configuration["user"])

    def on_welcome(self, bot):
        bot.send_message('nickserv', "identify {} {}".format(self.configuration["nickserv_account"], self.configuration["nickserv_password"]))
        time.sleep(5)
        for channel in self.configuration["channels"]:
            bot.join_channel(channel)
            time.sleep(1)

    def get_weather(self, message):
        if len(message.split()) > 1:
            weather_data = requests.get("http://api.apixu.com/v1/current.json",params={"key":self.configuration["weather_api_key"],"q":message.split(" ", 1)[1]}).json()
        if not 'error' in weather_data:
            return "The weather in {} is {} and {} degrees.".format(weather_data["location"]["name"], weather_data["current"]["condition"]["text"], weather_data["current"]["temp_c"])
        else:
            return "{}".format(weather_data["error"]["message"])

    def get_url_title(self, url):
        html = requests.get(url).text
        title_match = re.search("<title>(.*?)</title>", html)
        try:
            shortener = Shortener('Isgd')
            short_url = shortener.short(url)
        except:
            short_url = None
    
        if title_match and short_url:
            return "^ {} → {}".format(title_match.group(1), short_url)
        if title_match and short_url is None:
            return "^ {}".format(title_match.group(1))
        return 'Could not retrieve the title of the URL'

    def on_message(self, bot, channel, sender, message):
        try:
            if len(message.split()) == 0:
                message = "." #For people who try to crash bots with just spaces
            if message.split()[0] == ".weather":
                bot.send_message(channel, self.get_weather(message))
            if message.split()[0] == ".source":
                bot.send_message(channel, "My source code is here: https://github.com/buttbot-irc/buttbot")
            for message_part in message.split():
                if message_part.startswith("http://") or message_part.startswith("https://"):
                    bot.send_message(channel, self.get_url_title(message_part))
        except Exception as exception:
            bot.send_message(channel, "An error occurred, which has been logged.")
            bot.send_message(channel, "The following message:")
            bot.send_message("tinyhippo", "<{}> {}".format(sender, message))
            bot.send_message("tinyhippo", "{}".format(str(exception)))

    def on_private_message(self, bot, sender, message):
        print(message)

buttbot = Buttbot()


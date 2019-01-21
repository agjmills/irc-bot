#!/usr/bin/python3
# -*- coding: utf8 -*-
import JustIRC
import re
from pyshorteners import Shortener
import time
import yaml 
import os
import sys
import pkgutil
import Plugins
import requests
import importlib

class Buttbot:
    configuration = {}
    bot = None
    modules = []

    def __init__(self):
        self.configure()
        self.setup_bot()

    def setup_bot(self):
        self.bot =  JustIRC.IRCConnection()
        self.import_plugins('Plugins')
        self.bot.on_connect.append(self.on_connect)
        self.bot.on_welcome.append(self.on_welcome)
        self.bot.on_public_message.append(self.on_message)
        self.bot.connect("irc.freenode.net")
        try:
            self.bot.run_loop()
        except Exception as exception:
            self.bot.send_message("tinyhippo", "An error occurred, which has been logged.")
            self.bot.send_message("tinyhippo", "{}".format(str(exception)))
 
    def import_plugins(self, pkg_dir):
        for (module_loader, name, ispkg) in pkgutil.iter_modules([pkg_dir]):
            mod = importlib.import_module('.' + name, pkg_dir)
            self.bot.on_public_message.append(mod.on_message)
    
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

    def get_url_title(self, channel, bot, url):
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
            bot.send_message(channel, 'Could not retrieve the title of the URL')

    def on_message(self, bot, channel, sender, message):
        try:
            if len(message.split()) == 0:
                message = "." #For people who try to crash bots with just spaces
            if message.split()[0] == ".source":
                bot.send_message(channel, "My source code is here: https://github.com/buttbot-irc/buttbot")
            for message_part in message.split():
                if message_part.startswith("http://") or message_part.startswith("https://"):
                    self.get_url_title(channel, bot, message_part)
        except Exception as exception:
            bot.send_message(channel, "An error occurred, which has been logged.")
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            bot.send_message("tinyhippo", "The following message:")
            bot.send_message("tinyhippo", "<{}> {}".format(sender, message))
            bot.send_message("tinyhippo", "Caused the following exception:")
            bot.send_message("tinyhippo", "{}".format(str(exception)))
            bot.send_message("tinyhippo", "in file {} on line {}".format(fname, exc_tb.tb_lineno))

    def on_private_message(self, bot, sender, message):
        print(message)

buttbot = Buttbot()



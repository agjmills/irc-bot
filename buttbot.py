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
        self.bot.connect("irc.freenode.net")
        try:
            self.bot.run_loop()
        except Exception as exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.bot.send_message("tinyhippo", "An error occurred, which has been logged.")
            self.bot.send_message("tinyhippo", "{}".format(str(exception)))
            self.bot.send_message("tinyhippo", "in file {} on line {}".format(fname, exc_tb.tb_lineno))
 
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

    def on_private_message(self, bot, sender, message):
        print(message)

buttbot = Buttbot()



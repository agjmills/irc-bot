import sys
import os

def on_message(bot, channel, sender, message):
    if len(message.split()) == 0:
        message = "." #For people who try to crash bots with just spaces
    if message.split()[0] == ".restart" and sender == "tinyhippo":
        restart()

def restart():
    python = sys.executable
    os.execl(python, python, * sys.argv)

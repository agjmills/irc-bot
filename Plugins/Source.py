def on_message(bot, channel, sender, message):
    if len(message.split()) == 0:
        message = "." #For people who try to crash bots with just spaces
    if message.split()[0] == ".source":
        bot.send_message(channel, "My source code is here: https://github.com/agjmills/buttbot")

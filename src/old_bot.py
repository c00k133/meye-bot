#!/usr/bin/env python3

from telegram.ext import Updater, CommandHandler
import json, restrictions, sys, os


@restrictions.restricted
def start(bot, update):
    bot.sendMessage(
        chat_id=update.message.chat_id,
        text="I'm a bot, please talk to me!"
    )

@restrictions.restricted
def test(bot, update):
    bot.sendMessage(
        chat_id=update.message.chat_id,
        text="Testing"
    )

@restrictions.restricted
def image(bot, update):
    bot.send_photo(
        chat_id=update.message.chat_id,
        photo=open("image.jpg", "rb")
    )


def main():

    filepath = "../token.json"

    try:
        with open(filepath) as file_o:
            secrets = json.load(file_o)
    except IOError:
        print("Could not find {}.".format(filepath))

        
    token      = secrets["token"]
    updater    = Updater(token=token)
    dispatcher = updater.dispatcher

    print("\n" + ("-" * 40))
    
    print("Creating handlers.")
    start_handler = CommandHandler('start', start)
    image_handler = CommandHandler('image', image)
    test_handler  = CommandHandler('test', test)
    
    print("Adding handlers.")
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(image_handler)
    dispatcher.add_handler(test_handler)
    
    print("Started polling.")
    
    updater.start_polling()
    updater.idle()

    
    print(("-" * 40) + "\n")
    print("Done, bot running.")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("W: interrupt received, stopping...")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


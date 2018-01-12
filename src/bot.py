#!/urs/bin/env

from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler
import restrictions
import os, sys, shutil

CAM_DIR = '/var/lib/motioneye/'

class Bot:

    def __init__(self, token, name=None):
        self.name  = name

        self.updater    = Updater(token=token)
        self.dispatcher = self.updater.dispatcher
        self.dispatcher.add_handler(CommandHandler('start', self.start))

    @restrictions.restricted
    def start(self, bot, update):
        bot.send_message(
            chat_id=update.message.chat_id,
            text=self
        )

    @restrictions.restricted
    def cameras(self, bot, update):
        row = True
        camera_keyboard = [[]]
        for cam in os.listdir(CAM_DIR):
            if row:
                camera_keyboard[-1].append(cam)
            else: camera_keyboard.append([cam])
        reply_markup = ReplyKeyboardMarkup(camera_keyboard)
        bot.send_message(
            chat_id=update.message.chat_id,
            text="Cameras",
            reply_markup=reply_markup
        )

    def __str__(self):
        return "I'm {}, I'll look after you!".format(self.name if self.name else "a bot")

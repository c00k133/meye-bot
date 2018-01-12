#!/urs/bin/env

from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler
from datetime import timedelta
import restrictions
import os, sys, shutil

CAM_DIR = '/var/lib/motioneye/'

class Bot:

    def __init__(self, token, name=None):
        self.name  = name

        self.updater    = Updater(token=token)
        self.dispatcher = self.updater.dispatcher

        start_handler = CommandHandler('start', self.start)
        self.dispatcher.add_handler(start_handler)

        cameras_handler = CommandHandler('cameras', self.cameras)
        self.dispatcher.add_handler(cameras_handler)

        uptime_handler = CommandHandler('uptime', self.uptime)
        self.dispatcher.add_handler(uptime_handler)

#    @restrictions.restricted
    def start(self, bot, update):
        bot.send_message(
            chat_id=update.message.chat_id,
            text=self
        )

#    @restrictions.restricted
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

#    @restrictions.restricted
    def uptime(self, bot, update):
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readLines().split()[0])
            uptime_string  = str(timedelta(seconds - uptime_seconds))
        bot.send_message(
            chat_id=update.message.chat_id,
            text="My uptime has been:\n" + uptime_string
        )

    def run(self):
        self.updater.start_polling()

    def __str__(self):
        return "I'm {}, I'll look after you!".format(self.name if self.name else "a bot")

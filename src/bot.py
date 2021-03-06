#!/usr/bin/env

from telegram import ReplyKeyboardMarkup
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler
from datetime import timedelta
from functools import wraps
import os, telegram, nmap, time, requests 

CAM_DIR = '/var/lib/motioneye/'  # Default set by MotionEye
LIST_OF_USERS = []
TEST_USERS = []
MAC_ADDRESSES = {}

def restrict(func):
    @wraps(func)
    def wrapped(self, bot, update, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in LIST_OF_USERS:
            print('Unathorized access denied for {}.'.format(user_id))
            return
        return func(self, bot, update, *args, **kwargs)
    return wrapped

class Bot:

    def __init__(self, token, name=None):
        self.name = name

        self.bot        = telegram.Bot(token)
        self.updater    = Updater(token=token)
        self.dispatcher = self.updater.dispatcher

        # Start handlers
        ##########################################################

        start_handler = CommandHandler('start', self.start)
        self.dispatcher.add_handler(start_handler)

        test_handler = CommandHandler('test', self.test)
        self.dispatcher.add_handler(test_handler)

        cameras_handler = CommandHandler('cameras', self.cameras)
        self.dispatcher.add_handler(cameras_handler)

        uptime_handler = CommandHandler('uptime', self.uptime)
        self.dispatcher.add_handler(uptime_handler)

        athome_handler = CommandHandler('athome', self.athome)
        self.dispatcher.add_handler(athome_handler)

        get_ip_handler = CommandHandler('getip', self.get_ip)
        self.dispatcher.add_handler(get_ip_handler)

        # End handlers
        ##########################################################

    def _get_macs(self):
        nm = nmap.PortScanner()
        nm.scan(hosts='192.168.1.0/24', arguments='-sP')
        host_list = nm.all_hosts()
        online = []
        for host in host_list:
            temp = nm[host]['addresses']
            if 'mac' in temp and temp['mac'] in MAC_ADDRESSES.keys():
                online.append(MAC_ADDRESSES[temp['mac']])
        return online

    @restrict
    def start(self, bot, update):
        bot.send_message(
            chat_id=update.message.chat_id,
            text=self.__str__()
        )

    @restrict
    def test(self, bot, update):
        bot.send_message(
            chat_id=update.message.chat_id,
            text="testing"
        )

    @staticmethod
    def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
        menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
        if header_buttons:
            menu.insert(0, header_buttons)
        if footer_buttons:
            menu.append(footer_buttons)
        return menu

    @restrict
    def cameras(self, bot, update):
        cams = os.listdir(CAM_DIR)
        button_list = [KeyboardButton(cam) for cam in cams]
        reply_markup = InlineKeyboardMarkup(self.build_menu(buttons=button_list, n_cols=len(cams) % 3))
        bot.send_message(
            chat_id=update.message.chat_id,
            text='Cameras',
            reply_markup=reply_markup
        )

    @restrict
    def uptime(self, bot, update):
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
            uptime_string = str(timedelta(seconds=uptime_seconds))
        bot.send_message(
            chat_id=update.message.chat_id,
            text='My uptime has been:\n' + '<b>{}</b>'.format(uptime_string),
            parse_mode=telegram.ParseMode.HTML
        )

    def test_listen(self, msg='Received a message!'):
        # TODO: make so that messages are not sent if the admin is at home

        filepath    = CAM_DIR + 'Camera1'  # TODO: Change this so that additional cameras can be added
        newest_dir  = sorted(list(os.listdir(filepath)))[-1]
        actual_path = filepath + '/' +  newest_dir
        newest_file = sorted(list(os.listdir(actual_path)))
        the_file    = newest_file[-1]

        with open(actual_path + '/' + the_file, 'rb') as f:
            if '.thumb' in the_file:
                for user in TEST_USERS:
                    self.bot.send_photo(
                        chat_id=user,
                        photo=f,
                        caption=msg
                    )
            else:
                for user in TEST_USERS:
                    self.bot.send_video(
                        chat_id=user,
                        video=f,
                        caption=msg
                    )

    @restrict
    def athome(self, bot, update):
        self.bot.send_message(
            chat_id=update.message.chat_id,
            text='Started scanning'
        )
        start = time.time()
        now_online = self._get_macs()
        end = time.time()
        if len(now_online) == 0:
            text = 'Found none ({:.3f}s)'.format(end - start)
        else:
            text = "The following are at home ({:.3f}s):\n".format(end - start) + "\n".join(map(lambda usr: '@' + usr, now_online))
        self.bot.send_message(
            chat_id=update.message.chat_id,
            text=text
        )

    @restrict
    def get_ip(self, bot, update):
        r = requests.get(r'http://www.icanhazip.com')
        self.bot.send_message(
            chat_id=update.message.chat_id,
            text='Your current IP: ' + r.text
        )

    def run(self):
        self.updater.start_polling()
        for usr in TEST_USERS:
            self.bot.send_message(
                chat_id=usr,
                text='Bot has started'
            )

    def stop(self):
        print('Stopping the bot...')
        self.updater.stop()

    def __str__(self):
        return "I'm {}, I'll look after you!".format(self.name if self.name else "a bot")

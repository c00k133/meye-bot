#!/urs/bin/env

from telegram import ReplyKeyboardMarkup
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler
from datetime import timedelta
from functools import wraps
import os, telegram, nmap, time

CAM_DIR = '/var/lib/motioneye/'
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
        self.name  = name

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

        # End handlers
        ##########################################################

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
        def get_macs():
            nm = nmap.PortScanner()
            nm.scan(hosts='192.168.1.0/24', arguments='-e wlan0 -sP')
            host_list = nm.all_hosts()
            ls = []
            for host in host_list:
                temp = nm[host]['addresses']
                if 'mac' in temp:
                    ls.append(temp['mac'])
            online = []
            for mac in ls:
                if mac in MAC_ADDRESSES.keys():
                    online.append(MAC_ADDRESSES[mac])
            return online

        if update.effective_user.id in TEST_USERS:
            self.bot.send_message(
                chat_id=update.message.chat_id,
                text='Started scanning'
            )
            start = time.time()
            now_online = get_macs()
            end = time.time()
            if len(now_online) == 0:
                text = 'Found none ({}s)'.format(int(end - start))
            else:
                text = "The following are at home ({}s):\n".format(int(end - start)) + "\n".join(now_online)
            self.bot.send_message(
                chat_id=update.message.chat_id,
                text=text
            )

    def run(self):
        self.updater.start_polling()

    def stop(self):
        print('Stopping the bot...')
        self.updater.stop()

    def __str__(self):
        return "I'm {}, I'll look after you!".format(self.name if self.name else "a bot")

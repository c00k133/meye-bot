from telegram.ext import Updater, CommandHelper
import json, restrictions, sys, os

class Bot:
    def __init__(self, token, name=None):
        self.token = token
        self.name  = name

    def hello(self):
        pass

    def __str__(self):
        if self.name:
            return "Hi, I'm {}!".format(self.name)
        else:
            return "Hi, I'm a bot!"


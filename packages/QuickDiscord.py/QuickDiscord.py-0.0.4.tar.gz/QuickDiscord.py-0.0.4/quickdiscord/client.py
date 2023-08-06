import discord
from . import __version__


class Client():
    def __init__(self, prefix):
        self.version = __version__
        self.prefix = prefix

    def run(self, commandName: str):
        print(self.prefix + commandName)

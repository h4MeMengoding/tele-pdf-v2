'''

█ █▄ █    █▄█ ▄▀▄ █▄ ▄█ ██▀    █▀▄ █▀▄ █▀ 
█ █ ▀█    █ █ █▀█ █ ▀ █ █▄▄    █▀  █▄▀ █▀ 
                        Dev : IlhamGUD

'''

import logging
from pyromod import listen
from Configs.dm import Config
from pyrogram import Client, idle


# LOGGING INFO: DEBUG
logging.basicConfig(
    level = logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.ERROR)

# GLOBAL VARIABLES
PDF = {}            # save images for generating pdf
PROCESS = []        # to check current process
invite_link = None


# PLUGIN DIRECTORY
plugin = dict(
    root = "plugins"
)


# PYROGRAM BOT AUTHENTIFICATION
bot = Client(
    "InHamePDF",
    plugins = plugin,
    api_id = Config.API_ID,
    parse_mode = "markdown",
    api_hash = Config.API_HASH,
    bot_token = Config.API_TOKEN
)


bot.start()
idle()
bot.stop()

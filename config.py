from pathlib import Path

from config_reader import env

ENV_PATH = Path().home() / 'telegate/telegate.env'
IDENTITY_DB = Path().home() / 'telegate/identity.db'
BOT_TOKEN = env(ENV_PATH)['BOT_TOKEN']

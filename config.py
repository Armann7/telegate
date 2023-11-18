import os
from pathlib import Path

IDENTITY_DB = Path(os.environ['TELEGATE_DATA']) / 'identity.db'
BOT_TOKEN = os.environ['BOT_TOKEN']

from json import load
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ.get('TOKEN')

ADMIN_CHAT_ID = os.environ.get('ADMIN_CHAT_ID')

DATABASE_URL = os.environ.get('DATABASE_URL')

SERVER_MODE = 'test' #"test" Or "production"

WEBHOOK_URL = os.environ.get('WEBHOOK_URL')
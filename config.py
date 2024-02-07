import os
from dotenv import load_dotenv

# Tokens
load_dotenv()
API_TOKEN = os.getenv('BOT_TOKEN')

# Bot Configuration
TASK_DELETE_DURATION = 1
TASK_IDLE_DURATION = 30
TASK_UPDATE_DURATION = 5

# DB configuration
PG_PORT = os.getenv('POSTGRES_PORT')
PG_HOST = os.getenv('POSTGRES_HOST')
PG_PASSWORD = os.getenv('POSTGRES_PASSWORD')
PG_USER = os.getenv('POSTGRES_USER')
PG_DB = os.getenv('POSTGRES_DB')

ENVIRONMENT = os.getenv('ENV')

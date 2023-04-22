import os
from dotenv import load_dotenv 

## Tokens
load_dotenv()
API_TOKEN = os.getenv('BOT_TOKEN')

## Bot Configuration
TASK_DELETE_DURATION = 0.1
TASK_UPDATE_DURATION = 60
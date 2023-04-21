import os
from dotenv import load_dotenv 

## Tokens
load_dotenv()
API_TOKEN = os.getenv('BOT_TOKEN')

## Bot Configuration
TASK_DELETE_DURATION = 5
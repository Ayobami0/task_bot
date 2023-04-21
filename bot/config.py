import os
from dotenv import load_dotenv 

load_dotenv('.env')
API_TOKEN = os.getenv('BOT_TOKEN')

## Bot Configuration
TASK_DELETE_DURATION = 5
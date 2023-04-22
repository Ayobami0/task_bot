import logging
from telegram import (
    Update,
)
from telegram.ext import (
    ContextTypes,
)
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("""
Help Section for DewalletBot

### Commands ###
/start ==> start bot
/help ==> displays help section for dewallet bot
/tasks ==> generate the list of tasks resolved
/numberOfTasks => gives the number of the task
/generateRandomPin => generates a random pin for users. Email address of user is required
/changeActiveAgent => changes the shift to the sender of the command for easy notification
/changeActiveOperator => changes the member of operations current resolving complaint(operation team only)

### Rules ###
- Regular tasks should contain 'task' to indicate that they are a task
- Airtime for cash task should contain 'airtimeForCash'
- Bank payment task should contain 'payment'
- Verification issue should start with or contain 'verify'
""")
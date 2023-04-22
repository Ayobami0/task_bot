import logging

from telegram import (
    ForceReply,
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
)
from telegram.ext import (
    ContextTypes,
)
from models import task, task_list

async def tasks_number_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Send a message when the command /task_no is issued."""
    await update.message.reply_text(
        f"Task Created\nPENDINGS => {task_list.Tasks.get_pendings()}\n\
PROCESSING => {task_list.Tasks.get_processing()}\n\
CANCELED => {task_list.Tasks.get_canceled()}\n\
COMPLETED => {task_list.Tasks.get_resolved()}\n\
CLOSED => {task_list.Tasks.get_closed()}"
    )

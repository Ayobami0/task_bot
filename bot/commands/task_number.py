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

import database.operations as db
from models.status import Status

async def tasks_number_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Send a message when the command /task_no is issued."""
    await update.message.reply_text(
        f"Task Created\nPENDINGS => {db.read_by_status(Status.pending)}\n\
PROCESSING => {db.read_by_status(Status.processing)}\n\
CANCELED => {db.read_by_status(Status.canceled)}\n\
COMPLETED => {db.read_by_status(Status.resolved)}\n\
CLOSED => {db.read_by_status(Status.closed)}"
    )

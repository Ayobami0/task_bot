import logging
from telegram import (
    Update,
)
from telegram.ext import (
    ContextTypes,
)
import database.operations as db

async def get_tasks(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Return all tasks in a single message."""
    await update.message.reply_text(
        db.read_all()
    )

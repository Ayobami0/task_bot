import logging
from telegram import (
    Update,
)
from telegram.ext import (
    ContextTypes,
)
from models import task, task_list

async def get_tasks(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Return all tasks in a single message."""
    await update.message.reply_text(
        task_list.Tasks.get_all()
    )

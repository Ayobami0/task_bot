import logging

from telegram import (
    ForceReply,
    Update,
)
from telegram.ext import (
    ContextTypes,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!\n You can start creating task immediately. Tasks must include 'task' to be registered as a task. Use the command /help to get addtional information",
        reply_markup=ForceReply(selective=True),
    )

import logging
from telegram import (
    Update,
)
from telegram.ext import (
    ContextTypes,
)
from utils.random_pin import randomPin

async def generate_random_pin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Generates a random pin with the command /generateRandomPin"""

    await update.message.reply_text("Sure, what is the users email address?")

async def confirm_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Generates a random pin with the command /generateRandomPin"""

    await update.message.reply_text("Sure, what is the users email address?")

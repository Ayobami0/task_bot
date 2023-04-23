import logging

from telegram import ForceReply, Update
from telegram.ext import ContextTypes, ConversationHandler
from utils.random_pin import randomPin

CONFIRM_EMAIL = 0

async def generate_random_pin(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Generates a random pin with the command /generateRandomPin"""
    await update.message.reply_text(
        "Sure, what is the users email address?",
        reply_markup=ForceReply(selective=True),
    )
    return CONFIRM_EMAIL


async def confirm_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Generates a random pin with the command /generateRandomPin"""

    email = update.message.text
    pin = randomPin(4)
    await update.message.reply_text(f"The pin for {email}is\n\n{pin}")
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("%s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "You canceled the process. Check that the email is valid if you want to try again.", reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

async def failed(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles incorrect email entries, notifies sender and ends the conversation."""
    user = update.message.from_user
    await update.message.reply_text(
        "You entered an invalid email address. Check that the email is valid if you want to try again.", reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END
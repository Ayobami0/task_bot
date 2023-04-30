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
from bot_commands.delete import delete
from bot_commands.update import update as up
from config import TASK_DELETE_DURATION, TASK_UPDATE_DURATION
from utils.timer import CountDownExecutor


async def payments_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles payments with pictures of receipt"""
    task_creator = None
    query = update.callback_query
    message = update.effective_message
    chat_id = update.effective_chat.id
    message_id = message.id

    keyboard1 = [
        [
            InlineKeyboardButton("Confirming", callback_data="confirming"),
        ],
        [
            InlineKeyboardButton("Not Received", callback_data="not_received"),
        ],
        [
            InlineKeyboardButton("Credited", callback_data="credited"),
        ],
    ]
    keyboard2 = [
        [
            InlineKeyboardButton("Not Received", callback_data="not_received"),
        ],
        [
            InlineKeyboardButton("Credited", callback_data="credited"),
        ],
    ]
    keyboard3 = [
        [
            InlineKeyboardButton("Not Received", callback_data="not_received"),
        ],
        [
            InlineKeyboardButton("Credited", callback_data="credited"),
        ],
        [
            InlineKeyboardButton("Close", callback_data="closed"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard1)
    reply_markup2 = InlineKeyboardMarkup(keyboard2)
    reply_markup3 = InlineKeyboardMarkup(keyboard3)

    if query != None:
        await query.answer()
        message_id = message_id - 1
        match query.data:
            case "not_received":
                await query.message.edit_text(
                    f"{query.message.text}\nPayment not received. Ask customer to check back in {TASK_UPDATE_DURATION}mins. I'll Notify you then.",
                    reply_markup=reply_markup3,
                )
                CountDownExecutor(
                    TASK_UPDATE_DURATION,
                    up(
                        update.get_bot(),
                        task_creator,
                        message_id,
                        chat_id,
                        "I'm notifying you about this task",
                    ),
                ).run()
            case "confirming":
                await query.message.edit_text(
                    f"{query.message.text}\nConfirming Payment...",
                    reply_markup=reply_markup2,
                )
            case "credited":
                await query.message.edit_text(
                    f"{query.message.text}\nUser credited. Check user wallet to confirm.\nTask will be deleted in {TASK_DELETE_DURATION}mins"
                )
                CountDownExecutor(
                    TASK_DELETE_DURATION, delete(update.get_bot(), chat_id, message_id)
                ).run()
            case "closed":
                await query.message.edit_text(
                    f"{query.message.text}\nTask Closed.\nTask will be deleted in {TASK_DELETE_DURATION}mins"
                )
                CountDownExecutor(
                    TASK_DELETE_DURATION, delete(update.get_bot(), chat_id, message_id)
                ).run()
    else:
        if message.caption == None:
            await message.reply_text(
                "Add the payment information for the transaction as the image caption"
            )
        else:
            task_creator = update.message.from_user.name
            await message.reply_text(f"{message.caption}", reply_markup=reply_markup)
            await update.get_bot().pin_chat_message(chat_id, message_id)

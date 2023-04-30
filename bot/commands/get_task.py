import logging
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.ext import (
    ContextTypes,
)
import telegram.error as t_error

import database.operations as db


async def get_tasks(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Return all tasks in a single message."""
    query = update.callback_query
    page = 1

    page_buttons = [
        [
            InlineKeyboardButton('PREV', callback_data='previous_page'),
            InlineKeyboardButton('NEXT', callback_data='next_page'),
        ]
    ]

    page_markup = InlineKeyboardMarkup(page_buttons)

    if query is None:
        await update.message.reply_text(
            db.read_all(),
            reply_markup=page_markup if db.read_all(
            ) != 'There are no Tasks yet. Please create one' else None
        )
    else:
        await query.answer()
        match query.data:
            case 'previous_page':
                try:
                    page = page - 1
                except t_error.BadRequest:
                    logging.info('You are at the first page')
            case 'next_page':
                try:
                    page = page + 1
                except t_error.BadRequest:
                    logging.info('You are at the last page')
        await query.edit_message_text(db.read_all(page=page), reply_markup=page_markup)

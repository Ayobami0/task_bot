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
from utils.extract_task_information import extract_task
from utils.timer import CountDownExecutor
from config import TASK_DELETE_DURATION
from utils.random_pin import randomPin

async def verify_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard1 = [
        [
            InlineKeyboardButton('Yes', callback_data='yes'),
            InlineKeyboardButton('No', callback_data='no')
        ]
    ]
    keyboard2 = [
        [
            InlineKeyboardButton('Done', callback_data='verified')
        ]
    ]

    query = update.callback_query
    chat_id = update.effective_chat.id
    message = update.effective_message
    message_id = message.id
    
    reply_markup1 = InlineKeyboardMarkup(keyboard1)
    reply_markup2 = InlineKeyboardMarkup(keyboard2)

    if query == None:
        await message.reply_text(f'{message.text}\n\nMail Sent?', reply_markup=reply_markup1)
        await message.get_bot().pin_chat_message(chat_id, message_id)
    else:
        message_id = message_id - 1
        await query.answer()
        
        match query.data:
            case 'yes':
                await query.message.edit_text(f'{query.message.text}\nVerifying...Please Wait...', reply_markup=reply_markup2)
            case 'no':
                await query.message.edit_text(f'{query.message.text}\nAwaiting Mail...', reply_markup=reply_markup1)
            case 'verified':
                await query.message.edit_text(f'{query.message.text}\nUser Verified! Kindly Revert back to user\nTask will be deleted in {TASK_DELETE_DURATION}mins')
                CountDownExecutor(TASK_DELETE_DURATION, delete(update.get_bot(), chat_id, message_id)).run()

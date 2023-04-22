import logging

from bot_commands.delete import delete
from config import TASK_DELETE_DURATION
from models import task, task_list
from telegram import (ForceReply, InlineKeyboardButton, InlineKeyboardMarkup,
                      ReplyKeyboardMarkup, Update)
from telegram.ext import ContextTypes
from utils.extract_task_information import extract_task
from utils.random_pin import randomPin
from utils.timer import CountDownExecutor


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the task with inline buttons."""
    keyboard = [
        [
            InlineKeyboardButton("Process", callback_data="processing"),
            InlineKeyboardButton("Cancel", callback_data="cancel"),
        ],
    ]
    complete_keyboard = [
        [
            InlineKeyboardButton("Sent", callback_data="sent"),
            InlineKeyboardButton("Invalid", callback_data="invalid"),
        ],
        [
            InlineKeyboardButton("Refund", callback_data="refunded"),
            InlineKeyboardButton("Was Successful", callback_data="success"),
        ]
    ]
    resolved_keyboard = [
        [
            InlineKeyboardButton("Review", callback_data="review"),
            InlineKeyboardButton("Reverted", callback_data="reverted"),
        ]
    ]
    query = update.callback_query
    chat_id = update.effective_chat.id
    message = update.effective_message
    message_id = message.id

    if query == None:
        try :
            task_ = task.Task(extract_task(update.message.text))
            task_list.Tasks.add(task_, id_=message_id)
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.pin()

            await update.message.reply_text(update.message.text, reply_markup=reply_markup)
        except IndexError:
            await update.message.reply_text("""An invalid task format was entered. Created tasks should follow this format:
1. User's email address
2. Service amount (i.e 250 or 1000)
3. Sercice number (phone number, iuc number or meter number)
4. Service type (i.e MTN 1gb, GLO 20gb, Dstv Padi 2500)
5. Service date (the day the user placed the request)
6. Urgency (LOW, HIGH, MEDIUM [resellers are always registered as high])
7. Comments (additional information required)
    """)
    else:
        await query.answer()
        message_id = message_id - 2
        task_ = task_list.Tasks.get(message_id)

        copied_message = query.message
        reply_markup = InlineKeyboardMarkup(complete_keyboard)
        reply_resolved = InlineKeyboardMarkup(resolved_keyboard)

        match query.data:
            case "sent":
                task_.status = "RESOLVED"
                task_list.Tasks.update(message_id-2, task_)
                await query.edit_message_text(
                    text=f"{copied_message.text}\n\nTask resolved.",
                    reply_markup=reply_resolved,
                )
            case "refunded":
                task_.status = "RESOLVED"
                task_list.Tasks.update(message_id, task_)
                await query.edit_message_text(
                    text=f"{copied_message.text}\n\nUser refunded.",
                    reply_markup=reply_resolved,
                )
            case "invalid":
                task_.status = "RESOLVED"
                task_list.Tasks.update(message_id, task_)
                await query.edit_message_text(
                    text=f"{copied_message.text}\n\nInvalid details provided, check task an try again.",
                    reply_markup=reply_resolved,
                )
            case "success":
                task_.status = "RESOLVED"
                task_list.Tasks.update(message_id, task_)
                await query.edit_message_text(
                    text=f"{copied_message.text}\n\nWas successful the moment it was placed",
                    reply_markup=reply_resolved,
                )
            case "review" | "processing":
                task_.status = "PROCESSING"
                task_list.Tasks.update(message_id, task_)
                await query.edit_message_text(
                    text=f"{copied_message.text}\nTask is being processed",
                    reply_markup=reply_markup,
                )
            case "cancel":
                task_.status = "CANCELED"
                task_list.Tasks.update(message_id, task_)
                await query.edit_message_text(
                    text=f"{copied_message.text}\nTask canceled. Check task information and resend.\nThis task would be deleted in {TASK_DELETE_DURATION}mins",
                )
                # unpin message after deletion and completion
                CountDownExecutor(TASK_DELETE_DURATION, delete(update.get_bot(), chat_id, query.message.id)).run()
            case "reverted":
                task_.status = "CLOSED"
                task_list.Tasks.update(message_id, task_)
                await query.edit_message_text(
                    text=f"{copied_message.text}\nTask is closed\nThis task will be deleted in {TASK_DELETE_DURATION}mins",
                )
                CountDownExecutor(TASK_DELETE_DURATION, delete(update.get_bot(), chat_id, query.message.id)).run()
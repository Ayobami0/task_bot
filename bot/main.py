#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

import logging

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import (
    ForceReply,
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    Bot
)
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

from utils.extract_task_information import extract_task
from utils.timer import CountDownExecutor
from config import API_TOKEN, TASK_DELETE_DURATION
from models import task, task_list
from bot_commands.delete import delete

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def tasks_number_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Send a message when the command /task_no is issued."""
    await update.message.reply_text(
        f"Task Created\nPENDINGS => {task_list.Tasks.get_pendings()}\n\
PROCESSING => {task_list.Tasks.get_processing()}\n\
CANCELED => {task_list.Tasks.get_canceled()()}\n\
COMPLETED => {task_list.Tasks.get_resolved()}\n\
CLOSED => {task_list.Tasks.get_closed()}"
    )

async def get_tasks(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Return all tasks in a single message."""
    await update.message.reply_text(
        task_list.Tasks.get_all()
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the task with inline buttons."""

    task_ = task.Task(extract_task(update.message.text))
    print(update.message.id)
    task_list.Tasks.add(task_, id_=update.message.message_id)
    keyboard = [
        [
            InlineKeyboardButton("Process", callback_data="processing"),
            InlineKeyboardButton("Cancel", callback_data="cancel"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.pin()

    await update.message.reply_text(update.message.text, reply_markup=reply_markup)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text with a button."""

    complete_keyboard = [
        [
            InlineKeyboardButton("Complete?", callback_data="completed"),
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

    # CallbackQueries need to be answered, even if no notification to the user is needed
    await query.answer()
    id_ = query.message.id - 2
    task_ = task_list.Tasks.get(id_)
    print(task_, id_)

    copied_message = query.message
    reply_markup = InlineKeyboardMarkup(complete_keyboard)
    reply_resolved = InlineKeyboardMarkup(resolved_keyboard)

    match query.data:
        case "completed":
            task_.status = "RESOLVED"
            task_list.Tasks.update(id_, task_)
            await query.edit_message_text(
                text=f"{copied_message.text}\n\nTask resolved.",
                reply_markup=reply_resolved,
            )
        case "review" | "processing":
            task_.status = "PROCESSING"
            task_list.Tasks.update(id_, task_)
            await query.edit_message_text(
                text=f"{copied_message.text}\nTask is being processed",
                reply_markup=reply_markup,
            )
        case "cancel":
            task_.status = "CANCELED"
            task_list.Tasks.update(id_, task_)
            await query.edit_message_text(
                text=f"{copied_message.text}\nTask canceled. Check task information and resend.\nThis task would be deleted in {TASK_DELETE_DURATION}mins",
            )
            # unpin message after deletion and completion
            CountDownExecutor(TASK_DELETE_DURATION, delete(Bot(API_TOKEN), chat_id, id_)).run()
        case "reverted":
            task_.status = "CLOSED"
            task_list.Tasks.update(id_, task_)
            await query.edit_message_text(
                text=f"{copied_message.text}\nTask is closed\nThis task will be deleted in {TASK_DELETE_DURATION}mins",
            )
            await delete(Bot(API_TOKEN), chat_id, id_)

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = (
        Application.builder()
        .token(API_TOKEN)
        .build()
    )

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("tasks", get_tasks))
    application.add_handler(CommandHandler("tasksNos", tasks_number_command))
    application.add_handler(CallbackQueryHandler(button))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()

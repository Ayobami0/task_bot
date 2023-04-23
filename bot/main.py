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
    ConversationHandler,
)

from config import API_TOKEN, TASK_DELETE_DURATION
from filters.task_filter import AirtimeForCashFilter, PaymentsFilter

from commands.change_active_agent import change_active_agent, change_active_operator
from commands.generate_random_pin import generate_random_pin, confirm_email, cancel, CONFIRM_EMAIL, failed
from commands.get_task import get_tasks
from commands.help import help_command
from commands.start import start
from commands.task_number import tasks_number_command

from handlers.echo import echo
from handlers.payment import payments_handler
from handlers.verify_user import verify_user

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = (
        Application.builder()
        .token(API_TOKEN)
        .build()
    )

    # conversation handlers
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("generateRandomPin", generate_random_pin)], 
        states={
            CONFIRM_EMAIL: [MessageHandler(filters.Regex("^\w\w+.@+\w+\.\w+") & filters.TEXT, confirm_email)],
        }, 
        fallbacks=[
            MessageHandler(~filters.Regex("^\w\w+.@+\w+\.\w+") & filters.TEXT, failed),
            CommandHandler("cancel", cancel)
        ])

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("tasks", get_tasks))
    application.add_handler(CommandHandler("numberOfTasks", tasks_number_command))

    application.add_handler(CallbackQueryHandler(payments_handler, pattern='confirming|credited|not_received|closed'))
    application.add_handler(CallbackQueryHandler(verify_user, pattern='yes|no|verified'))
    application.add_handler(CallbackQueryHandler(echo))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.Regex('[Tt]+[askASK]{3}') & filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(MessageHandler(filters.Regex('[vV]+erify') & filters.TEXT & ~filters.COMMAND, verify_user))
    application.add_handler(MessageHandler(filters.PHOTO & PaymentsFilter() &  ~filters.COMMAND, payments_handler))
    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()

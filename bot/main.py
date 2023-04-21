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

from utils.extract_task_information import extract_task
from utils.timer import CountDownExecutor
from utils.random_pin import randomPin
from config import API_TOKEN, TASK_DELETE_DURATION
from models import task, task_list
from bot_commands.delete import delete
from filters.task_filter import TaskFilter

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

agent_on_shift = None
operation_on_shift = None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!\n You can start creating task immediately. Tasks must include 'task' to be registered as a task. Use the command /help to get addtional information",
        reply_markup=ForceReply(selective=True),
    )
async def change_active_agent(update: Update, contex: ContextTypes.DEFAULT_TYPE):
    """Change the active agent on shift"""
    agent_on_shift = update.message.from_user.name
    await update.message.reply_text(f'{agent_on_shift} is now on shift.')

async def change_active_(update: Update, contex: ContextTypes.DEFAULT_TYPE):
    """Change the active agent on shift"""
    agent_on_shift = update.message.from_user.name
    await update.message.reply_text(f'{agent_on_shift} is now on shift.')
    
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("""
Help Section for DewalletBot

### Commands ###
/start ==> start bot
/help ==> displays help section for dewallet bot
/tasks ==> generate the list of tasks resolved
/numberOfTasks => gives the number of the task
/generateRandomPin => generates a random pin for users. Email address of user is required
/changeActiveAgent => changes the shift to the sender of the command for easy notification
/changeActiveOperator => changes the member of operations current resolving complaint(operation team only)

### Rules ###
- Regular tasks should contain 'task' to indicate that they are a task
- Airtime for cash task should contain 'airtimeForCash'
- Bank payment task should contain 'payment'
- Verification issue should start with or contain 'verify'
""")

async def tasks_number_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Send a message when the command /task_no is issued."""
    await update.message.reply_text(
        f"Task Created\nPENDINGS => {task_list.Tasks.get_pendings()}\n\
PROCESSING => {task_list.Tasks.get_processing()}\n\
CANCELED => {task_list.Tasks.get_canceled()}\n\
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

async def payments_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles payments with pictures of receipt"""
    query = update.callback_query
    message = update.message
    keyboard1 = [
        [
            InlineKeyboardButton("Confirming", callback_data="confirming"),
        ],
        [
            InlineKeyboardButton("Not Received", callback_data="revert"),
        ],
        [
            InlineKeyboardButton("Credited", callback_data="credited"),
        ],
    ]
    keyboard2 = [
        [
            InlineKeyboardButton("Not Received", callback_data="revert"),
        ],
        [
            InlineKeyboardButton("Credited", callback_data="credited"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard1)
    reply_markup2 = InlineKeyboardMarkup(keyboard2)
    
    if query != None:
        await query.answer()
        await query.message.reply_photo(query.message.photo, caption=f"{query.message.text}", reply_markup=reply_markup2)
    else:
        await message.reply_photo(message.photo, caption=f"{message.text}", reply_markup=reply_markup)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the task with inline buttons."""

    try :
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

async def generate_random_pin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Generates a random pin with the command /generateRandomPin"""

    await update.message.reply_text("Sure, what is the users email address?")

async def confirm_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Generates a random pin with the command /generateRandomPin"""

    await update.message.reply_text("Sure, what is the users email address?")

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """handles all button queries and parses their callbacks"""

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

    # CallbackQueries need to be answered, even if no notification to the user is needed
    await query.answer()
    id_ = query.message.id - 2
    task_ = task_list.Tasks.get(id_)
    print(task_, id_)

    copied_message = query.message
    reply_markup = InlineKeyboardMarkup(complete_keyboard)
    reply_resolved = InlineKeyboardMarkup(resolved_keyboard)

    match query.data:
        case "sent":
            task_.status = "RESOLVED"
            task_list.Tasks.update(id_, task_)
            await query.edit_message_text(
                text=f"{copied_message.text}\n\nTask resolved.",
                reply_markup=reply_resolved,
            )
        case "refunded":
            task_.status = "RESOLVED"
            task_list.Tasks.update(id_, task_)
            await query.edit_message_text(
                text=f"{copied_message.text}\n\nUser refunded.",
                reply_markup=reply_resolved,
            )
        case "invalid":
            task_.status = "RESOLVED"
            task_list.Tasks.update(id_, task_)
            await query.edit_message_text(
                text=f"{copied_message.text}\n\nInvalid details provided, check task an try again.",
                reply_markup=reply_resolved,
            )
        case "success":
            task_.status = "RESOLVED"
            task_list.Tasks.update(id_, task_)
            await query.edit_message_text(
                text=f"{copied_message.text}\n\nWas successful the moment it was placed",
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
            CountDownExecutor(TASK_DELETE_DURATION, delete(update.get_bot(), chat_id, id_)).run()
        case "reverted":
            task_.status = "CLOSED"
            task_list.Tasks.update(id_, task_)
            await query.edit_message_text(
                text=f"{copied_message.text}\nTask is closed\nThis task will be deleted in {TASK_DELETE_DURATION}mins",
            )
            CountDownExecutor(TASK_DELETE_DURATION, delete(update.get_bot(), chat_id, id_)).run()

async def verify_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    verify_keyboard = [
        [
            InlineKeyboardButton('Yes', callback_data='yes'),
            InlineKeyboardButton('No', callback_data='no')
        ]
    ]

    verify_markup = InlineKeyboardMarkup(verify_keyboard)
    
    message = update.message

    await message.pin()

    await message.reply_text(f'{message.text}\n\nMail Sent?\n{message.from_user.name}', reply_markup=verify_markup)

async def verify_user_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    chat_id = update.effective_chat.id
    message_id = query.message.message_id - 2

    verify_keyboard = [
        [
            InlineKeyboardButton('Yes', callback_data='yes'),
            InlineKeyboardButton('No', callback_data='no')
        ]
    ]
    confirm_keyboard = [
        [
            InlineKeyboardButton('Done', callback_data='verified')
        ]
    ]

    confirm_markup = InlineKeyboardMarkup(confirm_keyboard)
    verify_markup = InlineKeyboardMarkup(verify_keyboard)

    await query.answer()
    
    match query.data:
        case 'yes':
            await query.message.edit_text(f'{query.message.text}\nVerifying...Please Wait...', reply_markup=confirm_markup)
        case 'no':
            await query.message.edit_text(f'{query.message.text}\nAwaiting Mail...', reply_markup=verify_markup)
        case 'verified':
            await query.message.edit_text(f'{query.message.text}\nUser Verified! Kindly Revert back to user\nTask will be deleted in {TASK_DELETE_DURATION}mins')
            CountDownExecutor(1, delete(update.get_bot(), chat_id, message_id)).run()

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
            # 'EMAIL': [MessageHandler(filters.Regex() & filters.TEXT, callback)],
            'CONFIRMATION': []
        }, 
        fallbacks=[])

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("tasks", get_tasks))
    application.add_handler(CommandHandler("numberOfTasks", tasks_number_command))
    application.add_handler(CallbackQueryHandler(verify_user_handler, pattern='yes|no|verified'))
    application.add_handler(CallbackQueryHandler(payments_handler, pattern='confirming|credited|revert'))
    application.add_handler(CallbackQueryHandler(button))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.Regex('[Tt]+[askASK]{3}') & filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(MessageHandler(filters.Regex('[vV]+erify') & filters.TEXT & ~filters.COMMAND, verify_user))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()

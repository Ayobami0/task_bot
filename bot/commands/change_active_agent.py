import logging
from telegram import (
    Update,
)
from telegram.ext import (
    ContextTypes,
)
agent_on_shift = None
operation_on_shift = None

async def change_active_agent(update: Update, contex: ContextTypes.DEFAULT_TYPE):
    """Change the active agent on shift"""
    agent_on_shift = update.message.from_user.name
    await update.message.reply_text(f'{agent_on_shift} is now on shift.')

async def change_active_operator(update: Update, contex: ContextTypes.DEFAULT_TYPE):
    """Change the active agent on shift"""
    agent_on_shift = update.message.from_user.name
    await update.message.reply_text(f'{agent_on_shift} is now on shift.')
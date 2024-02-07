from telegram import Bot

async def update(bot: Bot, to_user, message_id, chat_id, message):
    await bot.send_message(chat_id, f"Hi, {to_user}. {message}", reply_to_message_id=message_id)
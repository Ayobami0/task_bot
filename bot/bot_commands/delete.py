async def delete(bot, chat_id, message_id):
    await bot.unpin_chat_message(chat_id, message_id)
    await bot.delete_message(chat_id, message_id)
    await bot.delete_message(chat_id, message_id+2)
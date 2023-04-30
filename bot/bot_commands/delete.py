async def delete(bot, chat_id, message_id):
    await bot.unpin_chat_message(chat_id, message_id)
    await bot.delete_message(chat_id, message_id)  #Bot Reply message
    await bot.delete_message(chat_id, message_id-1)  #User message

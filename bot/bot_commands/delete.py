async def delete(bot_instance, chat_id, message_id):
    async with bot_instance as bot:
        await bot.unpin_chat_message(chat_id, message_id)
        await bot.delete_message(chat_id, message_id)
        await bot.delete_message(chat_id, message_id+2)
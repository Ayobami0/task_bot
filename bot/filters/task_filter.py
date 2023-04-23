from telegram import Message
from telegram.ext import filters
import re

class PaymentsFilter(filters.MessageFilter):
    def filter(self, message: Message) -> bool:
        try:
            if re.match('[Pp][aymentAYMENT]+', message.caption) != None:
                return True
        except TypeError:
            return False
        return False

class AirtimeForCashFilter(filters.MessageFilter):
    def filter(self, message: Message):
        try:
            if re.match('[Aa]4[Cc]', message.caption) != None:
                return True
        except TypeError:
            return False
        return False